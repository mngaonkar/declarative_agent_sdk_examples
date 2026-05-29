from declarative_agent_sdk import AgentFactory, AgentRegistry, AIAgentServer

agent = AgentFactory.from_yaml_file('configs/agent.yaml')
AgentRegistry.register(agent, category="news")

server = AIAgentServer(agent, host="0.0.0.0", port=8000)
server.run()

