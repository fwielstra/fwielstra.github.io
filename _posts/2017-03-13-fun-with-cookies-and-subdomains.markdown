---
layout:     post
title:      Fun with cookies and subdomains
date:       2017-03-13 12:00:00
summary:    A post about how browsers handle cookies with wildcard subdomains and how it may cause problems
tags:
 - browsers
 - cookies
 - security
---

Not too long ago, we ran into an apparent security issue at my current assignment - people could sign in with a regular account, but get the authentication and permissions of an administrator user (a priviledge escalation bug). As it turned out the impact was low, as the user would need to be logged in as an admin user already, but it was a very confusing issue. In this post I'll try and explain the situation, how browsers handle wildcard subdomain cookies, and what to keep in mind when building an authentication back-end.

First, some background information. We run a microservices architecture where security is handled via an authentication proxy of sorts; each request to any microservice passes through it, and it will check a JWT token cookie sent by the client. If the contents (a base64 encoded set of keys / values containing stuff like user ID, permissions, etc) match with a signature (signed by a private key in the authentication proxy), the request is forwarded to the actual microservice in question, enriched with a couple of headers containing the user's authentication information.

This service also handles authentication and manages the token cookie. When a user calls the `/authenticate` endpoint with a username / password combination, the service will in turn call the user management microservice to check the username / password. If the user service returns an OK, the authentication service will encode some user information (ID, etc) into a [JSON Web Token (JWT)](https://jwt.io/) cookie, sign it, and return it to the client via a `Set-Cookie` header.

Now, for reasons that have been forgotten by time, the token cookie has a `Domain` attribute set to a wildcard subdomain one level higher than the origin of the request. What this means is that if the user logged in via `www.example.com`, the `Domain` attribute of the cookie would be set to `.example.com`. I think this was to allow for sharing the token cookie between different development branches of the application.

Our development environment is served on URLs with a pattern of e.g. `some-feature.dev.example.com` Therefore, if the user logged in on one of those subdomains, a token cookie would be set for `.dev.example.com`.

The problem now became apparent when our admin tool became available on a new address - it became the equivalent of `admin.example.com`. This was a secondary application, but it uses the same authentication system. You can probably see where this is going now. When logging in to `admin.example.com`, a token cookie containing the admin account's information would be set with the domain `.example.com`. When logging in to `some-feature.dev.example.com` with a regular, non-admin account, a few things happened:

 * The token cookie for `.example.com`, containing the administrator's information, would be sent along with the regular user's authentication call. This didn't trigger any errors.
 * If the regular user's credentials were good, the authentication call would return a new token for `.dev.example.com`, containing the information for that user. This did not overwrite the token with the less specific Domain attribute, as described in [RFC 6265, section 4.1.2](https://tools.ietf.org/html/rfc6265#section-4.1.2).
 * Any consequent calls to the back-end would actually contain *two* token cookies, one for `.dev.example.com` with the regular user's JWT token, and one for `.example.com` containing the administrator's token.

We mainly discovered this by seeing one user name as logged in, but the information returned by the APIs belonged to an admin user. We found out the admin's token was returned by pulling the second part of the JWT token through a base64 decoder - note that JWT tokens are base64 encoded and signed, not encrypted. This issue was confusing as well because the username shown as the logged in user on the page was the regular, non-admin user; this name was returned by the call to the authentication endpoint, not fetched fresh from the server based on the token alone. This information was stored in local storage too, so a refresh did not update the information.

The back-end never considered a multiple-cookies-with-same-name scenario. Section [4.2.2 of RFC 6265](https://tools.ietf.org/html/rfc6265#section-4.2.2) does not forbid multiple cookies with the same name, but it also states that the server cannot make assumptions about the order, and that no metadata like domain, expiration, the secure flag, or anything will be sent along. Therefore, which token was used becomes pretty arbitrary and therefore, since it's used in authentication, insecure.

This issue affects both Chrome and Firefox, although the issue is a bit harder to debug in the latter; Chrome's `Application` tab in its dev tools will show both the `.example.com` and `.dev.example.com` cookies, but Firefox only seems to display the `.dev.example.com` cookie, after logging in to the dev application. The actual requests do contain both cookies though, so don't trust Firefox's Storage tab too much - I'd say this is a bug actually, I should report it somewhere.

The quick fix was simple enough; whenever two tokens are encountered in a request, the authentication service goes "I dunno, lol ¯\\\_(ツ)_/¯" and returns a 401 Unauthorized. This does put the user in limbo though; the current front-end application, when it receives a 401, will redirect the user to an error page; this triggers a DELETE call to the `authentication` endpoint, which in turn returns a `Set-Cookie` header that unsets the user's token cookie. However, it only does that for the subdomain-plus-one-level the user is currently on, not all domains. We did try to implement this, but it seems sending multiple `Set-Cookie` headers with the same name [is not allowed by the spec](https://tools.ietf.org/html/rfc6265#section-4.1), even if they have distinct `Domain` or `Path` attributes.

This also causes issues with a more proper fix. One very unwanted side-effect of storing a cookie with a wildcard subdomain is that the cookie is shared with other subdomains. In our case, we run our application on `app.example.com`, however the corporate website of our employer is running on `www.example.com`. This is another security issue, where token cookies are leaking out to `www.example.com`, not to mention all other subdomains - and the site is big enough that we do not know exactly who has access to it.

The more proper fix is to fix the cookie to only the subdomain that initiated the request. This is done by simply not sending a `Domain` attribute in the `Set-Token` header; browsers will fix the cookie to `application.example.com` then, without any wildcards; the token will not be available to either sibling subdomains (`www.example.com`) nor sub-subdomains (`dev.application.example.com`). This is easily implemented, however there will be existing users that still have the old subdomain token (`.example.com`); if those log in using the new `Domain` attribute, they will have two token cookies (`application.example.com` and `.example.com`), which will trigger the two-token-cookie authentication error. The clean solution would be to return two `Set-Cookie` headers, one that sets the new token to the full domain, one that unsets the old wildcard cookie. But that's not allowed.

What would work is to change the name of the token cookie, at least temporarily, to e.g. `token2`. This is probably what we are going to pursue, maybe changing it back to the old name once any old token cookies are expired (this would take about a week). The downside of that is that all users would be logged out and will need to log in again.

Another approach would be to add a 'token version' into the content of the JWT cookie. The authentication service can then decode both token cookies and check whether there is one with the current version, then use that one, letting the old cookie expire naturally.

So, in summary, some lessons learned:

 * Be careful with wildcard subdomains in cookies. I would recommend not using them to begin with; prefer full domain cookies, set them without a `Domain` attribute. If the intent is to create a single sign-on for development purposes, there are better ways.
 * You cannot send multiple `Set-Cookie` headers with the same name in one response.
 * You cannot practically change the domain of a (wildcard / subdomain) cookie with the same name.
 * The dev tools in Chrome and Firefox will report which cookies apply to the current domain differently; do not trust the `Storage` tabs in either browser's dev tools, but look at the actually sent `Cookie` request headers themselves. (It would be nice if the dev tools would format these in a more legible fashion)
 * The contents of a JWT token are not encrypted, only base64 encoded and signed; do not store critical information like passwords in a JWT cookie.
 * User data should not be stored in local storage if possible, not if it depends on a token which can change, be revoked, etc. Local storage also does not have an expiration date, unlike cookies, so it will persist until it's explicitly removed.
