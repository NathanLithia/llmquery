import discord
from discord.ext import commands
from discord import File
import io
import requests
import json

class llmquery(commands.Cog):
    """INSERT DESCRIPTION HERE"""
    def __init__(self, client):

        self.client = client
        self.promptmemory = "\n"
        self.sessionID = 0

        # Address of the LLM Service
        self.address = "192.168.0.100:5001"
        # Format of the LLM Service API
        self.api_url = f"http://{self.address}/api/v1/generate"
        # The first message sent to the LLM
        self.promptprogramming = "[The following is an interesting chat message log between NathanLithia and Lithia.]\n"
        # `n`: Number of responses to generate.
        self.n = 1
        # `max_context_length`: Max tokens to consider for context.
        self.max_context_length = 4096
        # `max_length`: Max tokens for the generated response.
        self.max_length = 220
        # `rep_pen`: Repetition penalty to discourage repeating tokens.
        self.rep_pen = 1.07
        # `temperature`: Controls randomness of output (higher = more random).
        self.temperature = 0.7
        # `top_p`: Nucleus sampling probability threshold.
        self.top_p = 0.92
        # `top_k`: Number of top-k tokens to sample from.
        self.top_k = 100
        # `top_a`: Select top `a` tokens based on their rank.
        self.top_a = 0
        # `typical`: Typical sampling to balance creativity and likelihood.
        self.typical = 1
        # `tfs`: Temperature sampling with a softmax filter.
        self.tfs = 1
        # `rep_pen_range`: Range for repetition penalty (affects position/frequency).
        self.rep_pen_range = 360
        # `rep_pen_slope`: Slope of repetition penalty (penalty escalation).
        self.rep_pen_slope = 0.7
        # `sampler_order`: Defines the order of token sampling.
        self.sampler_order = [6,0,1,3,4,2,5]
        # `memory`: Controls context memory retention during generation.
        self.memory = ""
        # `trim_stop`: Trims the output based on stop sequence or criteria.
        self.trim_stop = True
        # `genkey`: Generation key for controlling output determinism.
        self.genkey = "KCPP4972"
        # `min_p`: Minimum probability threshold for token selection.
        self.min_p = 0
        # `dynatemp_range`: Dynamic temperature range adjustment during generation.
        self.dynatemp_range = 0
        # `dynatemp_exponent`: Exponential effect for dynamic temperature adjustment.
        self.dynatemp_exponent = 1
        # `smoothing_factor`: Smooths token probabilities to encourage diversity.
        self.smoothing_factor = 0
        # `banned_tokens`: List of tokens/words to avoid generating.
        self.banned_tokens = []
        # `render_special`: Handle special tokens or formatting in output.
        self.render_special = False
        # `logprobs`: Return log probabilities of generated tokens.
        self.logprobs = False
        # `presence_penalty`: Penalize repeated token presence to encourage diversity.
        self.presence_penalty = 0
        # `logit_bias`: Adjust logits to influence specific token probabilities.
        self.logit_bias = {}
        # `quiet`: Suppress verbose/debug output during generation.
        self.quiet = False
        # `stop_sequence`: Token sequence that stops text generation.
        self.stop_sequence = ["NathanLithia:","\nNathanLithia ","\nLithia: "]
        # `use_default_badwordsids`: Use predefined list of bad words for filtering.
        self.use_default_badwordsids = False
        # `bypass_eos`: Skip end-of-sequence token to continue generating text.
        self.bypass_eos = False


    @commands.command(pass_context=True, aliases=['gpt'])
    async def llm(self, ctx, *, message):
        """Query LLM"""
        self.promptmemory = f"{self.promptmemory}\nNathanLithia: {message}\nLithia:"
        payload = {
        "n": self.n,
        "max_context_length": self.max_context_length,
        "max_length": self.max_length,
        "rep_pen": self.rep_pen,
        "temperature": self.temperature,
        "top_p": self.top_p,
        "top_k": self.top_k,
        "top_a": self.top_a,
        "typical": self.typical,
        "tfs": self.tfs,
        "rep_pen_range": self.rep_pen_range,
        "rep_pen_slope": self.rep_pen_slope,
        "sampler_order": self.sampler_order,
        "memory": self.memory,
        "trim_stop": self.trim_stop,
        "genkey": self.genkey,
        "min_p": self.min_p,
        "dynatemp_range": self.dynatemp_range,
        "dynatemp_exponent": self.dynatemp_exponent,
        "smoothing_factor": self.smoothing_factor,
        "banned_tokens": self.banned_tokens,
        "render_special": self.render_special,
        "logprobs": self.logprobs,
        "presence_penalty": self.presence_penalty,
        "logit_bias": self.logit_bias,
        "prompt": f"{self.promptprogramming}{self.promptmemory}",
        "quiet": self.quiet,
        "stop_sequence": self.stop_sequence,
        "use_default_badwordsids": self.use_default_badwordsids,
        "bypass_eos": self.bypass_eos
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
    async def llmclear(self,ctx):
        self.promptmemory = "\n"
        await ctx.send(f'Memory cleared!')


    @commands.command(pass_context=True)
    async def llmdebug(self, ctx):
        try:
            await ctx.reply(file=File(fp=io.StringIO(f"{self.promptprogramming}{self.promptmemory}"), filename="history.json"))
        except Exception as e: await ctx.send(f'{e}')



async def setup(client):
    await client.add_cog(llmquery(client))
