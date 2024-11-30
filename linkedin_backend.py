class LinkedInSignInSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, write_only=True)

    def get_linkedin_access_token(self, code) -> dict:
        """Generate LinkedIn access token using the code."""
        client_id = ""
        client_secret = ""
        redirect_uri = "http://localhost:3000/linkedin"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = f"""https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}"""

        try:
            response = requests.post(url, headers=headers)
            json_response = response.json()
            # If invalid request raise an error
            if response.status_code != 200:
                raise ValueError(json_response)
            # Return the valid response
            return json_response

        except Exception as e:
            raise serializers.ValidationError(e)

    def get_user_linkedin_profile(self, access_token) -> dict:
        """Get LinkedIn user profile using the access token."""
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://api.linkedin.com/v2/me"
        try:
            response = requests.get(url, headers=headers)
            json_response = response.json()
            if response.status_code != 200:
                raise ValueError(json_response)

            return json_response

        except Exception as e:
            raise serializers.ValidationError(e)

    def get_linkedin_userinfo(self, access_token) -> dict:
        """Get LinkedIn user information using the access token."""
        headers = {"Authorization": f"Bearer {access_token}"}
        url = "https://api.linkedin.com/v2/userinfo"
        try:
            response = requests.get(url, headers=headers)
            json_response = response.json()
            if response.status_code != 200:
                raise ValueError(json_response)

            return json_response

        except Exception as e:
            raise serializers.ValidationError(e)

    def validate_code(self, code):
        """Check if the code is valid."""
        linkedin_access_token = self.get_linkedin_access_token(code).get("access_token")
        linkedin_userinfo = self.get_linkedin_userinfo(linkedin_access_token)
        # Return user information if the code is valid
        return linkedin_userinfo

    def create(self, validated_data):
        userinfo = validated_data.pop("code")
        return validated_data
