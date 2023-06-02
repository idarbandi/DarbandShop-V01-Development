import sys
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AYbKjWoEP4DFEa56DVTdRMB1j1xNg4XMnTyRizjCP4z0d99m9tRvDJKmxsoso9NCzB8T3Cr9CzhTmcew"
        self.client_secret = "EK1zSqDtGM0lBbI8sP5oPeubmKEI8HHeE1O5luSSH8OJqOKak4hdlo15bB-ig3SMcpGJaF4pbx_A34nd"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
