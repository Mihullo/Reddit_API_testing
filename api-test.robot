*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    String

Suite Setup    Request OAuth Token

*** Variables ***
${BASE_URL_NO_AUTH}  https://www.reddit.com
${PERSONAL_ID}  zQpVbSN7IQ7YcjOcxKMDaw
${SECRET_TOKEN}  9gLP0XqaRkfdlO5LXV3fOSexpDnEeA
${ACCESS_TOKEN}  api/v1/access_token
${BASE_URL}  https://oauth.reddit.com

&{HEADERS}      user-agent=MyTestScript by For_test_API
&{USER_DATA}    grant_type=password     username=For_test_API   password=1qaz@WSX

@{TROPHIE}      Verified Email  New User

*** Test Cases ***
Check Account Identification
    ${content}=     Get Handler Response Content    api/v1/me

    Dictionary Should Contain Item      ${content}     name    ${USER_DATA}[username]   msg=The username does not match!

Check Account Friends
    ${content}=     Get Handler Response Content    api/v1/me/friends

    Dictionary Should Contain Key      ${content}     kind  msg=The title does not match!
    Dictionary Should Contain Key      ${content}     data  msg=No data available!

Check Account Karma
    ${content}=     Get Handler Response Content    api/v1/me/karma

    Dictionary Should Contain Item      ${content}     kind    KarmaList   msg=The title does not match!

Check Account Trophies
    ${content}=     Get Handler Response Content    api/v1/me/trophies

    Dictionary Should Contain Item      ${content}      kind    TrophyList  msg=The title does not match!

*** Keywords ***
Request OAuth Token
    ${url}=         Format String    ${BASE_URL_NO_AUTH}/${ACCESS_TOKEN}
    @{auth}=        Create List    ${PERSONAL_ID}  ${SECRET_TOKEN}
    Create Session  OAuth  ${url}  headers=&{HEADERS}  auth=@{auth}     verify=True

    ${resp}=        POST On Session  OAuth  ${url}  data=&{USER_DATA}
    Status Should Be  200  ${resp}

    ${json}=        evaluate    json.loads('''${resp.content}''')    json
    ${acc_token}=   Get From Dictionary   ${json}  access_token
    ${token}=       Format String    bearer {}  ${acc_token}
    Set To Dictionary   ${HEADERS}  Authorization  ${token}

Get Handler Response Content
    [Arguments]     ${handler}

    ${url}=         Format String    ${BASE_URL}/${handler}
    ${resp}=        GET   ${url}   headers=${HEADERS}
    Status Should Be  200  ${resp}   msg=Request error!

    ${json}=        evaluate    json.loads('''${resp.content}''')    json
    RETURN          ${json}
