import React from "react";
import styled from "styled-components";
import { useLinkedIn } from "react-linkedin-login-oauth2";
import linkedin from "react-linkedin-login-oauth2/assets/linkedin.png";

function LinkedInPage() {
  const { linkedInLogin } = useLinkedIn({
    clientId: "",
    redirectUri: `${window.location.origin}/linkedin`,
    onSuccess: (code) => {
      console.log(code);
      setCode(code);
      setErrorMessage("");
    },
    scope: "openid profile r_ads_reporting r_organization_social rw_organization_admin w_member_social r_ads w_organization_social rw_ads r_basicprofile r_organization_admin email r_1st_connections_size",
    onError: (error) => {
      console.log(error);
      setCode("");
      setErrorMessage(error.errorMessage);
    },
  });
  const [code, setCode] = React.useState("");
  const [errorMessage, setErrorMessage] = React.useState("");

  return (
    <Wrapper>
      <img
        onClick={linkedInLogin}
        src={linkedin}
        alt="Log in with Linked In"
        style={{ maxWidth: "180px", cursor: "pointer" }}
      />

      {!code && <div>No code</div>}
      {code && (
        <div>
          <div>Authorization Code: {code}</div>
          <div>
            Follow{" "}
            <Link
              target="_blank"
              href="https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?context=linkedin%2Fconsumer%2Fcontext&tabs=HTTPS#step-3-exchange-authorization-code-for-an-access-token"
              rel="noreferrer"
            >
              this
            </Link>{" "}
            to continue
          </div>
        </div>
      )}
      {errorMessage && <div>{errorMessage}</div>}
    </Wrapper>
  );
}

const Wrapper = styled.div`
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Link = styled.a`
  font-size: 20px;
  font-weight: bold;
`;

export default LinkedInPage;
