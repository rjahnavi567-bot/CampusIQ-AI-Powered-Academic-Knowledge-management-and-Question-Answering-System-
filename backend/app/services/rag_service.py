from services.llm_service import LLMService


class RAGService:

    def __init__(self, vector_service):
        self.vector_service = vector_service
        self.llm_service = LLMService()

    def answer_question(
        self,
        question: str,
        marks: int = 5
    ):

        results = self.vector_service.search(
            query=question,
            top_k=3
        )

        context = "\n\n".join(
            chunk["text"]
            for chunk in results
        )

        answer = self.llm_service.generate_answer(
            question=question,
            context=context,
            marks=marks
        )

        return {
            "answer": answer,
            "sources": [
                {
                    "document": chunk["document"],
                    "page": chunk["page"]
                }
                for chunk in results
            ]
        }