from declarative_agent_sdk import AgentFactory, AgentRegistry

agent = AgentFactory.from_yaml_file('configs/agent.yaml')
AgentRegistry.register(agent, category="poetry")
result = agent.run_sync("download beautiful nebula image")
response = result.get("final_response", "")

print(response)
