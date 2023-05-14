# travel-marketplace-gpt
Practical use cases of applying GPT into a travel marketplace. This is a work-in-progress document.

## Use Case 1: Use GPT to improve search capabilities

In this use case, we will utilize the GPT embedding text feature to embed all trip plans' data. Every time a user searches with something, use the embedding text feature to embed the user's query as well. Use a semantic search method using the embed user's query on the embeded trip plans' data. Based on the given trip plans ranked from the most similarity to the least, we'll get the relevant local travel designers, destinations, travel themes, travel guides, and travel inspirations (blog posts) to present a holistic search result listing page.

In this use case, we'll explore several level of implementation difficulties, including
- Using pre-embeded csv file as the data source.
- Using either Pinecone or Chroma to manage the data source with LlamaIndex as the interface.
- Using the similarity model of OpenAI to perform the semantic search.
- Using OpenSearch or ElasticSearch to perform the semantic search.

## Use Case 2: Build a chatbot based on GPT to answer the travel questions

This chatbot can help answer the general questions around travelling to any specific destinations and/or of doing specific travel themes (adventure, sightseeing, food-tour...).

It is broken into 2 small itierations
1. Answer using GPT's knowledge
2. Combine with the knowledge of the travel marketplace to form the answer. The knowledge lies in the trip plan, the travel guide, and the travel inspirations.

We will demonstrate the ability of this chatbot to detect when the user is about to enquire so that we can present a link to the Enquiry Capture form for him/her to fill in the travel request.

## Use Case 3: Based on the inputted enquiry's details, ask the relevant questions to be able to present the most relevant trip plan or generate one to suggest the local travel designer to review and quote

## Use Case 4: Use GPT to assist the writing of trip's overview and highlights

## Use Case 5: Use GPT to determine whether the quoted price for a given trip plan is competitive

## Use Case 6: Use GPT for automatic review of the submitted trip plan to the enquiry's details

## Use Case 7: Use GPT to highlight how the submitted trip plan matches with the enquiry's details so the traveler can quickly determine whether to book

Moreover, use GPT to answer the FAQs around the marketplace policy and payment terms so that the traveler is 100% confident to deposit.

## Use Case 8: User Retargeting

## Use Case 9: Improve the SEO of the public trip plans
