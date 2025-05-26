#!/usr/bin/python3

"""
Script to send notification to g-space via Webhook
"""

import requests
import argparse
import sys


def build_message(message, thread=None, build_status=None):
    """Build message content.
    @param message: Message to send
    @param thread: Thread key to send message in thread
    @param build_status: Build status to use emojis in message (optional)
    """
    if build_status:
        message = "{} {}: {}".format(message_emoji(build_status), build_status.upper() ,message)
    content = {"text": message.strip()}
    if thread:
        content["thread"] = {"threadKey": "{}".format(thread)}
    return content


def message_emoji(status):
    """Get emoji for message based on status.
    @param status: Status of the build
    """
    if status.lower() == 'completed':
        status = "success"

    emoji_dict = {
        "started": "🛫",
        "success": "🏁",
        "failure": "🔥",
        "unstable": "⚠️",
        "aborted": "🔨"
    }

    return emoji_dict.get(status.lower())


def send_message(args):
    """Post message in Google Chat.
    @param args: User arguments from cli
    """
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    url = "https://chat.googleapis.com/v1/spaces/{}/messages?key={}&token={}".format(args.space_id, args.api_key, args.api_token)
    if args.thread:
        url += '&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD'
    try:
        requests.post(url, headers=headers, json=build_message(args.message, args.thread, args.build_status))
    except Exception as error:
        print("ERROR: Notification to g-chat failed")
        sys.exit(0)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Send notification to Google Chat")
    parser.add_argument("-k", "--api_key", help="API Key for Google Chat", default='AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI')
    parser.add_argument("-t", "--api_token", help="API Token for Google Chat", required=True)
    parser.add_argument("-s", "--space_id", help="Google chat space ID", required=True)
    parser.add_argument("-m", "--message", help="Message to send", required=True)
    parser.add_argument("-T", "--thread", help="Thread key to send message in thread", default=None)
    parser.add_argument("-S", "--build_status", help="Build status to use emojis in message", default=None)
    return parser.parse_args()


if __name__ == '__main__':
    """Do all things"""
    args = parse_args()
    send_message(args)
