from typing import Optional

from theflow.utils.modules import import_dotted_string

from kotaemon.base import Param

from .base import BaseEmbeddings, Document, DocumentWithEmbedding


class BaseOpenAIEmbeddings(BaseEmbeddings):
    """Base interface for OpenAI embedding model, using the openai library.

    This class exposes the parameters in resources.Chat. To subclass this class:

        - Implement the `prepare_client` method to return the OpenAI client
        - Implement the `openai_response` method to return the OpenAI response
        - Implement the params relate to the OpenAI client
    """

    _dependencies = ["openai"]

    api_key: str = Param(help="API key", required=True)
    timeout: Optional[float] = Param(None, help="Timeout for the API request.")
    max_retries: Optional[int] = Param(
        None, help="Maximum number of retries for the API request."
    )

    dimensions: Optional[int] = Param(
        None,
        help=(
            "The number of dimensions the resulting output embeddings should have. "
            "Only supported in `text-embedding-3` and later models."
        ),
    )

    @Param.auto(depends_on=["max_retries"])
    def max_retries_(self):
        if self.max_retries is None:
            from openai._constants import DEFAULT_MAX_RETRIES

            return DEFAULT_MAX_RETRIES
        return self.max_retries

    def prepare_input(
        self, text: str | list[str] | Document | list[Document]
    ) -> list[Document]:
        if isinstance(text, (str, Document)):
            return [Document(content=text)]
        elif isinstance(text, list):
            return [Document(content=_) for _ in text]
        return text

    def prepare_client(self, async_version: bool = False):
        """Get the OpenAI client

        Args:
            async_version (bool): Whether to get the async version of the client
        """
        raise NotImplementedError

    def openai_response(self, client, **kwargs):
        """Get the openai response"""
        raise NotImplementedError

    def invoke(
        self, text: str | list[str] | Document | list[Document], *args, **kwargs
    ) -> list[DocumentWithEmbedding]:
        input_ = self.prepare_input(text)
        client = self.prepare_client(async_version=False)
        resp = self.openai_response(
            client, input=[_.text if _.text else " " for _ in input_], **kwargs
        ).dict()
        output_ = sorted(resp["data"], key=lambda x: x["index"])
        return [
            DocumentWithEmbedding(embedding=o["embedding"], content=i)
            for i, o in zip(input_, output_)
        ]

    async def ainvoke(
        self, text: str | list[str] | Document | list[Document], *args, **kwargs
    ) -> list[DocumentWithEmbedding]:
        input_ = self.prepare_input(text)
        client = self.prepare_client(async_version=True)
        resp = await self.openai_response(
            client, input=[_.text if _.text else " " for _ in input_], **kwargs
        ).dict()
        output_ = sorted(resp["data"], key=lambda x: x["index"])
        return [
            DocumentWithEmbedding(embedding=o["embedding"], content=i)
            for i, o in zip(input_, output_)
        ]


class OpenAIEmbeddings(BaseOpenAIEmbeddings):
    """OpenAI chat model"""

    base_url: Optional[str] = Param(None, help="OpenAI base URL")
    organization: Optional[str] = Param(None, help="OpenAI organization")
    model: str = Param(
        help=(
            "ID of the model to use. You can go to [Model overview](https://platform."
            "openai.com/docs/models/overview) to see the available models."
        ),
        required=True,
    )

    def prepare_client(self, async_version: bool = False):
        """Get the OpenAI client

        Args:
            async_version (bool): Whether to get the async version of the client
        """
        params = {
            "api_key": self.api_key,
            "organization": self.organization,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries_,
        }
        if async_version:
            from openai import AsyncOpenAI

            return AsyncOpenAI(**params)

        from openai import OpenAI

        return OpenAI(**params)

    def openai_response(self, client, **kwargs):
        """Get the openai response"""
        params: dict = {
            "model": self.model,
        }
        if self.dimensions:
            params["dimensions"] = self.dimensions
        params.update(kwargs)

        return client.embeddings.create(**params)


class AzureOpenAIEmbeddings(BaseOpenAIEmbeddings):
    azure_endpoint: str = Param(
        help=(
            "HTTPS endpoint for the Azure OpenAI model. The azure_endpoint, "
            "azure_deployment, and api_version parameters are used to construct "
            "the full URL for the Azure OpenAI model."
        )
    )
    azure_deployment: str = Param(help="Azure deployment name", required=True)
    api_version: str = Param(help="Azure model version", required=True)
    azure_ad_token: Optional[str] = Param(None, help="Azure AD token")
    azure_ad_token_provider: Optional[str] = Param(None, help="Azure AD token provider")

    @Param.auto(depends_on=["azure_ad_token_provider"])
    def azure_ad_token_provider_(self):
        if isinstance(self.azure_ad_token_provider, str):
            return import_dotted_string(self.azure_ad_token_provider, safe=False)

    def prepare_client(self, async_version: bool = False):
        """Get the OpenAI client

        Args:
            async_version (bool): Whether to get the async version of the client
        """
        params = {
            "azure_endpoint": self.azure_endpoint,
            "api_version": self.api_version,
            "api_key": self.api_key,
            "azure_ad_token": self.azure_ad_token,
            "azure_ad_token_provider": self.azure_ad_token_provider_,
            "timeout": self.timeout,
            "max_retries": self.max_retries_,
        }
        if async_version:
            from openai import AsyncAzureOpenAI

            return AsyncAzureOpenAI(**params)

        from openai import AzureOpenAI

        return AzureOpenAI(**params)

    def openai_response(self, client, **kwargs):
        """Get the openai response"""
        params: dict = {
            "model": self.azure_deployment,
        }
        if self.dimensions:
            params["dimensions"] = self.dimensions
        params.update(kwargs)

        return client.embeddings.create(**params)
