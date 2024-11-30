class LinkedInSignInSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, write_only=True)

    def send_request(self, method, url, headers=None) -> dict:
        """
        Method for send HTTP requests and handle errors.
        """
        try:
            method_requests = {"POST": requests.post, "GET": requests.get}
            response = method_requests.get(method.upper())(url, headers=headers)
            response_data = response.json()

            # Raise an error for non-200 status codes
            if response.status_code != 200:
                response_data["status_code"] = response.status_code
                raise ValueError(response_data)

            return response_data

        except Exception as e:
            raise serializers.ValidationError(e)

    def fetch_access_token(self, code) -> dict:
        """
        Fetch LinkedIn access token using the provided authorization code.
        """
        client_id = "86cut14s0g5ayc"
        client_secret = "WPL_AP1.cLaBxeTBms9Xh629.uXCj0Q=="
        redirect_uri = "http://localhost:3000/linkedin"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Generate the access token URL
        url = (
            f"https://www.linkedin.com/oauth/v2/accessToken?"
            f"grant_type=authorization_code&code={code}&client_id={client_id}"
            f"&client_secret={client_secret}&redirect_uri={redirect_uri}"
        )

        return self.send_request("POST", url, headers=headers)

    def fetch_user_profile(self) -> dict:
        """
        Fetch LinkedIn user profile information using the access token.
        """
        url = "https://api.linkedin.com/v2/me"
        return self.send_request("GET", url, headers=self.headers)

    def fetch_user_email(self) -> dict:
        """
        Fetch LinkedIn user email information using the access token.
        """
        url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
        return self.send_request("GET", url, headers=self.headers)

    def fetch_user_info(self) -> dict:
        """
        Fetch LinkedIn user information using the access token.
        """
        url = "https://api.linkedin.com/v2/userinfo"
        return self.send_request("GET", url, headers=self.headers)

    def validate_code(self, value):
        """
        Validate the provided LinkedIn authorization code and return user info.
        """
        linkedin_access_token = self.fetch_access_token(value).get("access_token")
        self.headers = {"Authorization": f"Bearer {linkedin_access_token}"}
        user_info = self.fetch_user_info()

        return user_info

    def create(self, validated_data):
        """
        Create a new user instance using the validated data.
        """
        userinfo = validated_data.pop("code")

        """
        We can create a new user instance here using the validated data.
        """

        return validated_data
