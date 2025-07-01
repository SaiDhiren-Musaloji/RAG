import os
from dotenv import load_dotenv
from pathlib import Path
from mistral_inference.transformer import Transformer
from mistral_inference.generate import generate
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest

load_dotenv()

# Define the path where the model will be downloaded
mistral_models_path = Path.home().joinpath('mistral_models', '7B-Instruct-v0.3')

# Initialize tokenizer and model globally to avoid re-loading on each call
tokenizer = MistralTokenizer.from_file(str(mistral_models_path.joinpath('tokenizer.model.v3')))
model = Transformer.from_folder(mistral_models_path)

# Note: mistral_inference handles device placement internally, no explicit .to(device) needed

class ResearchAnalyzer:
    def __init__(self):
        # No API key needed for local model
        pass

    def filter_and_analyze(self, query: str, articles: list[str]) -> str:
        """
        Filters relevant information from articles and generates a 'What, When, How, Why' analysis report 
        using a locally run Mistral 7B model via mistral_inference.
        """
        filtered_information = []

        # First pass: Filter relevant information from each article
        for i, article_content in enumerate(articles):
            # Mistral instruct format
            filter_prompt_content = f"""
            You are a research assistant. Read the following article carefully.
            Extract ALL facts, events, and statements that are directly relevant to answering the research query: "{query}".
            List the extracted information clearly, sentence by sentence or as concise points.
            If no information is relevant, state 'No relevant facts found'.

            Article {i+1}:
            {article_content}

            Extracted Relevant Information:
            """
            
            completion_request = ChatCompletionRequest(messages=[UserMessage(content=filter_prompt_content)])
            encoded_prompt_tokens = tokenizer.encode_chat_completion(completion_request).tokens

            try:
                # Generate response using mistral_inference
                output_tokens, _ = generate(
                    [encoded_prompt_tokens],
                    model,
                    max_tokens=1000,
                    temperature=0.7,
                    top_p=0.9,
                    eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id # Ensure eos_id is used
                )
                extracted_text = tokenizer.decode(output_tokens[0]).strip()
                if extracted_text.lower() != "no relevant facts found" and extracted_text.strip():
                    filtered_information.append(f"Source {i+1}:\n{extracted_text}")
            except Exception as e:
                print(f"Error filtering article {i+1}: {str(e)}")
                continue

        if not filtered_information:
            return "No relevant information found for the query to generate a report."

        combined_filtered_text = "\n\n".join(filtered_information)

        # Second pass: Generate the comprehensive analysis report
        analysis_prompt_content = f"""
        You are an AI research analyst. Based on the following filtered information related to the query: "{query}", generate a comprehensive analysis report with the following sections:

        1.  **What:** Describe the core topic, key entities, and main concepts.
        2.  **When:** Provide any relevant timelines, historical context, or future projections.
        3.  **How:** Explain mechanisms, processes, methodologies, or approaches.
        4.  **Why:** Discuss reasons, causes, motivations, impacts, or implications.

        Ensure the report is well-structured, clear, concise, and directly addresses the query. Only use information provided in the filtered texts. If a section has no relevant information, state 'N/A' for that section.

        Filtered Information:
        {combined_filtered_text}

        Comprehensive Analysis Report:
        """
        
        completion_request = ChatCompletionRequest(messages=[UserMessage(content=analysis_prompt_content)])
        encoded_analysis_tokens = tokenizer.encode_chat_completion(completion_request).tokens

        try:
            output_tokens, _ = generate(
                [encoded_analysis_tokens],
                model,
                max_tokens=2000, # Increased tokens for detailed report
                temperature=0.7,
                top_p=0.9,
                eos_id=tokenizer.instruct_tokenizer.tokenizer.eos_id # Ensure eos_id is used
            )
            return tokenizer.decode(output_tokens[0]).strip()
        except Exception as e:
            return f"Error generating analysis report with Mistral: {str(e)}" 