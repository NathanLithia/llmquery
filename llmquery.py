import discord
from discord.ext import commands
import requests
import json

class llmquery(commands.Cog):
    """INSERT DESCRIPTION HERE"""
    def __init__(self, client):
        self.client = client
        self.address = "192.168.0.114:5001"
        self.api_url = f"http://{self.address}/api/v1/generate"
        self.sessionID = 0
        self.promptprogramming = "[The following is an interesting chat message log between NathanLithia and Lithia.]\n"
        self.promptmemory = "\n"

    @commands.command(pass_context=True, aliases=['gpt'])
    async def llm(self, ctx, *, message):
        """Query LLM"""
        self.promptmemory = f"{self.promptmemory}\nNathanLithia: {message}\nLithia:"
        payload = {
        "n": 1,
        "max_context_length": 4096,
        "max_length": 220,
        "rep_pen": 1.07,
        "temperature": 0.7,
        "top_p": 0.92,
        "top_k": 100,
        "top_a": 0,
        "typical": 1,
        "tfs": 1,
        "rep_pen_range": 360,
        "rep_pen_slope": 0.7,
        "sampler_order": [6,0,1,3,4,2,5],
        "memory": "",
        "trim_stop": True,
        "genkey": "KCPP4972",
        "min_p": 0,
        "dynatemp_range": 0,
        "dynatemp_exponent": 1,
        "smoothing_factor": 0,
        "banned_tokens": [],
        "render_special": False,
        "logprobs": False,
        "presence_penalty": 0,
        "logit_bias": {},
        "prompt": f"{self.promptprogramming}{self.promptmemory}",
        "quiet": False,
        "stop_sequence": ["NathanLithia:","\nNathanLithia ","\nLithia: "],
        "use_default_badwordsids": False,
        "bypass_eos": False
        }
        #json_payload = json.dumps(payload)
        try:
            response = requests.post(
                self.api_url, 
                json=payload, 
                headers={"Content-Type": "application/json"},
                timeout=10
                )
            response.raise_for_status()  # Raise an exception for 4xx/5xx errors
            # Parse and display the response
            generated_text = response.json()["results"][0]["text"]
            self.promptmemory = f"{self.promptmemory}{generated_text}"
            await ctx.reply(f"{generated_text}")
        except Exception as e: await ctx.send(f'{e}')

    @commands.command(pass_context=True)
    async def llmdebug(self, ctx):
        await ctx.send(f'```{self.promptprogramming}``` ```{self.promptmemory}```')



async def setup(client):
    await client.add_cog(llmquery(client))

