import os 
import pandas as pd 
import tiktoken
import asyncio
import nest_asyncio
from rich import print 
from graphrag.query.indexer_adapters import read_indexer_entities, read_indexer_reports
from graphrag.query.llm.oai.chat_openai import ChatOpenAI 
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.global_search.community_context import GlobalCommunityContext 
from graphrag.query.structured_search.global_search.search import GlobalSearch
from graphrag.query.indexer_adapters import (
    read_indexer_covariates,
    read_indexer_relationships,
    read_entities,
    read_indexer_reports,
    read_text_units,
)
import chainlit as cl 
from graphrag.query.input.loaders.dfs import (store_entity_semantic_embeddings,)

nest_asyncio.apply()

api_key = os.environ['GRAPHRAG_API_KEY']
llm_model = "gpt-3.5-turbo-0125"
llm = ChatOpenAI(
    api_key=api_key, 
    model=llm_model,
    api_type=OpenaiApiType.OpenAI,
    max_retries=5,
)
token_encoder = tiktoken.get_encoding('cl100k_base')

INPUT_DIR = r"C:\Users\Administrator\Documents - \Desktop\administrator\output\20240706-082527\artifacts"
COMMUNITY_REPORT_TABLE = "create_final_community_reports.parquet"
ENTITY_TABLE = "create_final_nodes.parquet"
ENTITY_EMBEDDING_TABLE = "create_final_entities.parquet"
TEXT_UNIT_TABLE = 'create_final_text_units.parquet'
RELATIONSHIPS_TABLE = 'create_final_relationships.parquet'

COMMUNITY_LEVEL = 0 
entity_df = pd.read_parquet(os.path.join(INPUT_DIR, ENTITY_TABLE))
report_df = pd.read_parquet(os.path.join(INPUT_DIR, COMMUNITY_REPORT_TABLE))
entity_embedding_df = pd.read_parquet(os.path.join(INPUT_DIR, ENTITY_EMBEDDING_TABLE))
relationship_df = pd.read_parquet(os.path.join(INPUT_DIR, RELATIONSHIPS_TABLE))

reports = read_indexer_reports(report_df, entity_df, COMMUNITY_LEVEL)
entities = read_indexer_entities(entity_df,entity_embedding_df, COMMUNITY_LEVEL)
relationships = read_indexer_relationships(relationship_df)

context_builder = GlobalCommunityContext( 
    community_reports=reports,
    entities=entities,
    token_encoder=token_encoder,
)

context_builder_params = {
    "use_community_summary": False,  
    "shuffle_data": True,
    "include_community_rank": True,
    "min_community_rank": 0,
    "community_rank_name": "rank",
    "include_community_weight": True,
    "community_weight_name": "occurrence weight",
    "normalize_community_weight": True,
    "max_tokens": 3_000,  
    "context_name": "Reports",
}

map_llm_params = {
    "max_tokens": 1000,
    "temperature": 0.0,
    "response_format": {"type": "json_object"},
}

reduce_llm_params = {
    "max_tokens": 2000,  
    "temperature": 0.0,
}

search_engine = GlobalSearch(
    llm=llm,
    context_builder=context_builder,
    token_encoder=token_encoder,
    max_data_tokens=12_000, 
    map_llm_params=map_llm_params,
    reduce_llm_params=reduce_llm_params,
    allow_general_knowledge=False,  
    json_mode=True, 
    context_builder_params=context_builder_params,
    concurrent_coroutines=10,
    response_type="multiple-page report",  
)

async def main(query):
    result = await search_engine.asearch(query)
    return result 

@cl.on_chat_start
async def start():
    await cl.Message("How can I assist you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    query = message.content
    result = await main(query)
    print(result.response)
    print(result.context_data['reports'])
    print(f'LLM calls: {result.llm_calls}.  LLM tokens: {result.prompt_tokens}')
    response = result.response 
    await cl.Message(content=response).send()

if __name__ == '__main__':
    cl.run(port=8080)