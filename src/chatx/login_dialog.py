# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import DialogTurnResult, ComponentDialog, DialogContext
from botbuilder.core import BotFrameworkAdapter
from botbuilder.schema import ActivityTypes

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
)
from botbuilder.dialogs.prompts import OAuthPrompt, OAuthPromptSettings


class LoginDialog(ComponentDialog):
    def __init__(self, connection_name: str):
        super(LoginDialog, self).__init__(LoginDialog.__name__)

        self.connection_name = connection_name

        self.add_dialog(
            OAuthPrompt(
                OAuthPrompt.__name__,
                OAuthPromptSettings(
                    connection_name=connection_name,
                    text="Please Sign In",
                    title="Sign In",
                    timeout=300000,
                ),
            )
        )

        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [self.prompt_step, self.login_step],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def prompt_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.begin_dialog(OAuthPrompt.__name__)

    async def login_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Get the token from the previous step. Note that we could also have gotten the
        # token directly from the prompt itself. There is an example of this in the next method.
        if step_context.result:
            return await step_context.end_dialog(step_context.result.token)

        await step_context.context.send_activity(
            "Login was not successful please try again."
        )
        return await step_context.begin_dialog(OAuthPrompt.__name__)

    async def on_begin_dialog(
        self, inner_dc: DialogContext, options: object
    ) -> DialogTurnResult:
        result = await self._interrupt(inner_dc)
        if result:
            return result
        return await super().on_begin_dialog(inner_dc, options)

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        result = await self._interrupt(inner_dc)
        if result:
            return result
        return await super().on_continue_dialog(inner_dc)

    async def _interrupt(self, inner_dc: DialogContext):
        if inner_dc.context.activity.type == ActivityTypes.message:
            text = inner_dc.context.activity.text.lower()
            if text == "logout":
                bot_adapter: BotFrameworkAdapter = inner_dc.context.adapter
                await bot_adapter.sign_out_user(inner_dc.context, self.connection_name)
                await inner_dc.context.send_activity("You have been signed out.")
                return await inner_dc.cancel_all_dialogs()
