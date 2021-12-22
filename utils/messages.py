import random
import re
from io import BytesIO
from typing import List, Optional, Union

import discord
from discord.errors import HTTPException
from discord.ext.commands import Context

moderation = [
    727365670395838626
]

NEGATIVE_REPLIES = ["Something wrong went", "Facing some issues"]


async def send_attachments(
    message: discord.Message,
    destination: Union[discord.TextChannel, discord.Webhook],
    link_large: bool = True,
    use_cached: bool = False,
    **kwargs,
) -> List[str]:
    """
    Re-upload the message's attachments to the destination and return a list of their new URLs.
    Each attachment is sent as a separate message to more easily comply with the request/file size
    limit. If link_large is True, attachments which are too large are instead grouped into a single
    embed which links to them. Extra kwargs will be passed to send() when sending the attachment.
    """
    webhook_send_kwargs = {
        "username": message.author.display_name,
        "avatar_url": message.author.avatar_url,
    }
    webhook_send_kwargs.update(kwargs)
    webhook_send_kwargs["username"] = sub_clyde(webhook_send_kwargs["username"])

    large = []
    urls = []
    for attachment in message.attachments:
        failure_msg = f"Failed to re-upload attachment {attachment.filename} from message {message.id}"

        try:
            # Allow 512 bytes of leeway for the rest of the request.
            # This should avoid most files that are too large,
            # but some may get through hence the try-catch.
            if attachment.size <= destination.guild.filesize_limit - 512:
                with BytesIO() as file:
                    await attachment.save(file, use_cached=use_cached)
                    attachment_file = discord.File(file, filename=attachment.filename)

                    if isinstance(destination, discord.TextChannel):
                        msg = await destination.send(file=attachment_file, **kwargs)
                        urls.append(msg.attachments[0].url)
                    else:
                        await destination.send(
                            file=attachment_file, **webhook_send_kwargs
                        )
            elif link_large:
                large.append(attachment)
            else:
                pass
        except HTTPException as e:
            if link_large and e.status == 413:
                large.append(attachment)
            else:
                pass

    if link_large and large:
        desc = "\n".join(
            f"[{attachment.filename}]({attachment.url})" for attachment in large
        )
        embed = discord.Embed(description=desc)
        embed.set_footer(text="Attachments exceed upload size limit.")

        if isinstance(destination, discord.TextChannel):
            await destination.send(embed=embed, **kwargs)
        else:
            await destination.send(embed=embed, **webhook_send_kwargs)

    return urls


def sub_clyde(username: Optional[str]) -> Optional[str]:
    """
    Replace "e"/"E" in any "clyde" in `username` with a Cyrillic "е"/"E" and return the new string.
    Discord disallows "clyde" anywhere in the username for webhooks. It will return a 400.
    Return None only if `username` is None.
    """

    def replace_e(match: re.Match) -> str:
        char = "е" if match[2] == "e" else "Е"
        return match[1] + char

    if username:
        return re.sub(r"(clyd)(e)", replace_e, username, flags=re.I)
    else:
        return username  # Empty string or None


async def send_denial(ctx: Context, reason: str) -> None:
    """Send an embed denying the user with the given reason."""
    embed = discord.Embed()
    embed.colour = discord.Colour.red()
    embed.title = random.choice(NEGATIVE_REPLIES)
    embed.description = reason

    await ctx.send(embed=embed)


def format_user(user: discord.abc.User) -> str:
    """Return a string for `user` which has their mention and ID."""
    return f"{user.mention} (`{user.id}`)"