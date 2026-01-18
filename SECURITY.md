# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of AI News Hub seriously. If you have discovered a security vulnerability, we appreciate your help in disclosing it to us responsibly.

### How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **Email**: Send an email to [security@ainewshub.dev](mailto:security@ainewshub.dev)
2. **GitHub Security Advisories**: Use [GitHub's private vulnerability reporting](https://github.com/ai-news/ai-news/security/advisories/new)

### What to Include

Please include the following information in your report:

- **Description**: A clear description of the vulnerability
- **Impact**: The potential impact of the vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Affected Versions**: Which versions are affected
- **Suggested Fix**: If you have one, a suggested fix or mitigation

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Target**: Within 90 days (depending on severity)

### What to Expect

1. **Acknowledgment**: We'll acknowledge your report within 48 hours
2. **Assessment**: Our security team will assess the vulnerability
3. **Updates**: We'll keep you informed of our progress
4. **Fix**: We'll work on a fix and coordinate disclosure
5. **Credit**: We'll credit you in our security advisory (unless you prefer to remain anonymous)

## Security Best Practices

### For Users

1. **Keep Updated**: Always use the latest version of AI News Hub
2. **API Keys**: Never commit API keys or secrets to repositories
3. **Access Control**: Use appropriate access controls for your deployment
4. **Audit Logs**: Regularly review logs for suspicious activity

### For Self-Hosted Deployments

1. **HTTPS**: Always use HTTPS in production
2. **Firewall**: Restrict access to database and Redis ports
3. **Environment Variables**: Never hardcode secrets
4. **Regular Updates**: Keep dependencies updated
5. **Backups**: Regularly backup your database

### For Contributors

1. **Input Validation**: Always validate and sanitize inputs
2. **SQL Injection**: Use parameterized queries (SQLAlchemy handles this)
3. **XSS Prevention**: Sanitize user-generated content
4. **No Hardcoded Secrets**: Never hardcode secrets in code
5. **Dependency Review**: Review security of new dependencies

## Security Features

AI News Hub includes several security features:

- **Authentication**: JWT-based authentication with refresh tokens
- **Password Hashing**: Bcrypt with appropriate cost factor
- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Server-side validation with Pydantic
- **CORS**: Configurable CORS policy
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Prevention**: React's built-in XSS protection

## Vulnerability Disclosure Policy

- We follow responsible disclosure practices
- We will not take legal action against researchers who follow this policy
- We will work with researchers to understand and resolve issues quickly
- We will credit researchers who report valid vulnerabilities

## Known Security Considerations

### Crawler Security

When adding new data source crawlers:
- Validate and sanitize all scraped content
- Use rate limiting to avoid overwhelming sources
- Handle timeouts and errors gracefully
- Don't execute any scraped JavaScript

### AI Processing Security

When using LLM APIs:
- Never include sensitive user data in prompts
- Validate LLM outputs before displaying
- Monitor for prompt injection attempts

---

Thank you for helping keep AI News Hub and our users safe!
