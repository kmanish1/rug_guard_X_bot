class VouchChecker:
    def __init__(self, api_client):
        self.api_client = api_client
        self.trusted_ids = [
            "123456789", "987654321", "456789123",
            "789123456", "321654987"  # Update with real IDs
        ]

    def check_trust_status(self, user_id):
        vouch_count = 0
        for trusted_id in self.trusted_ids:
            followers = self.api_client.get_users_followers(id=user_id)
            if followers.data and trusted_id in [f.id for f in followers.data]:
                vouch_count += 1
        return vouch_count >= 3