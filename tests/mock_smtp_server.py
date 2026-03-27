import asyncio
from aiosmtpd.controller import Controller

class MockHandler:
    async def handle_DATA(self, server, session, envelope):
        print('--- New Email Received ---')
        print(f'From: {envelope.mail_from}')
        print(f'To: {envelope.rcpt_tos}')
        print('Message Data:')
        print(envelope.content.decode('utf-8'))
        print('---------------------------')
        return '250 OK'

if __name__ == '__main__':
    handler = MockHandler()
    # Listen on localhost:1025
    controller = Controller(handler, hostname='127.0.0.1', port=1025)
    controller.start()
    print("Mock SMTP server running on 127.0.0.1:1025")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()
