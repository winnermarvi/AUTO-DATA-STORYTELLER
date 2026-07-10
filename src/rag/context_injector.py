def build_context(retrieved_documents):

    context = ""

    for document in retrieved_documents:

        context += f"""
            ========================================
            DOCUMENT TYPE
            ========================================
            {document['type']}

            CONTENT
            ----------------------------------------
            {document['content']}

            METADATA
            ----------------------------------------
            {document['metadata']}

        """

    return context