class Supervisor:
    def __init__(self, graham_output, optimizer_output, sentiment_output):
        self.graham_output = graham_output
        self.optimizer_output = optimizer_output
        self.sentiment_output = sentiment_output

    def analysis_agent(self):
        agent = ClaudeAgent(f"""You are an expert financial analyst who excels at everything.
                            Analyze what is given to you and provide a final summary and why to invest in these stocks by
                            looking at the inputs given from the user.""",
                            f"""Analyze the stocks from these inputs and tell me why it is a good investment.
                            This is the stocks that fit graham's analysis: {self.graham_output},
                            This is the optimizers for the selected stocks: {self.optimizer_output},
                            This is the sentiment analysis for the given stocks: {self.sentiment_output}.
                            Provide a summary and why to invest in them.""", api_key)
        return agent.send_request()
    
    def chat_with_user(self, user_prompt):
        analysis = self.analysis_agent()

        agent = ClaudeAgent(f"""You are an assistant, you can talk to the user and if the user asked you to output the best stock to invest then give him this output: {analysis}, otherwise if he did not ask 
                            for it then do not give it to him, speak to him freely and do what he asks you to do.""",
                            user_prompt, api_key)
        return agent.send_request()
    