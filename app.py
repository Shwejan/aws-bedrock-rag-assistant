import boto3
from botocore.exceptions import ClientError

# ---------------------------------------------------------
# AWS configuration
# ---------------------------------------------------------

REGION = "us-east-1"

# Your Amazon Bedrock Managed Knowledge Base ID
KNOWLEDGE_BASE_ID = "KLXDWROQJA"

# Amazon Nova Lite foundation model
MODEL_ID = "us.amazon.nova-lite-v1:0"


# ---------------------------------------------------------
# AWS clients
# ---------------------------------------------------------

bedrock_agent_runtime = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name=REGION
)


# ---------------------------------------------------------
# Retrieve relevant document chunks from Managed KB
# ---------------------------------------------------------

def retrieve_documents(question):
    print("Retrieving relevant documents from Bedrock Knowledge Base...")
    print("=" * 60)

    response = bedrock_agent_runtime.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={
            "text": question
        },
        retrievalConfiguration={
            "managedSearchConfiguration": {
                "numberOfResults": 5
            }
        }
    )

    results = response.get("retrievalResults", [])

    chunks = []
    sources = []

    for result in results:
        content = result.get("content", {})
        text = content.get("text", "")

        if text:
            chunks.append(text)

        location = result.get("location", {})
        s3_location = location.get("s3Location", {})
        uri = s3_location.get("uri")

        if uri and uri not in sources:
            sources.append(uri)

    return chunks, sources


# ---------------------------------------------------------
# Generate answer using Amazon Nova
# ---------------------------------------------------------

def generate_answer(question, chunks):
    if not chunks:
        return "I could not find relevant information in the knowledge base."

    context = "\n\n---\n\n".join(chunks)

    prompt = f"""
Use only the information in the context below to answer the question.

If the answer is not available in the context, say:
"I could not find that information in the knowledge base."

Question:
{question}

Context:
{context}

Provide a concise and accurate answer.
"""

    response = bedrock_runtime.converse(
        modelId=MODEL_ID,
        system=[
            {
                "text": (
                    "You are an enterprise policy assistant. "
                    "Answer questions only using the supplied retrieved context."
                )
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        inferenceConfig={
            "maxTokens": 300,
            "temperature": 0.1,
            "topP": 0.9
        }
    )

    return response["output"]["message"]["content"][0]["text"]


# ---------------------------------------------------------
# Main application
# ---------------------------------------------------------

def main():
    question = "How many vacation days do full-time employees receive?"

    print()
    print("AWS Bedrock RAG Knowledge Assistant")
    print("=" * 60)
    print(f"Knowledge Base ID: {KNOWLEDGE_BASE_ID}")
    print(f"Question: {question}")
    print()

    try:
        chunks, sources = retrieve_documents(question)

        print(f"Retrieved {len(chunks)} relevant chunks.")
        print()

        answer = generate_answer(question, chunks)

        print("Answer:")
        print(answer)

        print()
        print("Sources:")

        if sources:
            for source in sources:
                print(f"- {source}")
        else:
            print("- No S3 source URI returned")

    except ClientError as error:
        print()
        print("AWS Error:")
        print(error)

    except Exception as error:
        print()
        print("Unexpected Error:")
        print(error)


if __name__ == "__main__":
    main()