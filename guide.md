# Project Organization Guide

This repository structure is designed to organize projects by their **primary purpose**, not by programming language, framework, or technology stack.

## Root Structure

```text
root/
├── Projects/
│   ├── Web/
│   ├── Mobile/
│   ├── Desktop/
│   ├── APIs/
│   ├── Automation/
│   ├── AI/
│   ├── Libraries/
│   └── ReverseEngineering/
│
├── Archives/
└── Templates/
```

## Classification Principle

Always classify a project based on:

> **What is the main purpose of the project?**

Do not classify based on:

- Programming language
- Framework
- Database
- Deployment target
- Whether it exposes an API

A project should belong to the category that best represents its primary function.

## Categories

### Web

Applications primarily accessed through a web browser.

Examples:

- Portfolio websites
- Landing pages
- E-commerce websites
- Dashboards
- CMS platforms
- Blogs
- Web applications

### Mobile

Applications designed for smartphones and tablets.

Examples:

- Android applications
- iOS applications
- Cross-platform mobile apps

### Desktop

Applications intended to run on desktop operating systems.

Examples:

- Productivity tools
- Download managers
- Desktop utilities
- Local business software

### APIs

Projects whose primary purpose is to provide backend services or endpoints.

Examples:

- Authentication services
- Payment services
- Inventory APIs
- Notification services
- API gateways
- Reverse proxies

### Automation

Projects that automate tasks, extract data, process information, or perform scheduled work.

Examples:

- Scrapers
- Crawlers
- Bots
- ETL pipelines
- Synchronization tools
- Monitoring services
- Download link extractors
- Scheduled jobs

### AI

Projects whose primary value comes from artificial intelligence, machine learning, or advanced data processing.

Examples:

- LLM applications
- RAG systems
- Chatbots
- NLP projects
- Recommendation engines
- Computer vision systems
- Vector search systems

### Libraries

Reusable code intended to be imported or consumed by other projects.

Examples:

- SDKs
- Utility packages
- Shared components
- Internal frameworks
- Common helper modules

### ReverseEngineering

Projects related to analyzing, understanding, or modifying existing software, protocols, or systems.

Examples:

- APK analysis
- Binary analysis
- Protocol research
- Firmware analysis
- Malware research
- Network reverse engineering

## Classification Priority

```text
AI
↓
ReverseEngineering
↓
Automation
↓
APIs
↓
Web / Mobile / Desktop
↓
Libraries
```

## Decision Rule

Ask yourself:

> If I remove the API layer, what is the project fundamentally doing?

- If it is still scraping, extracting, syncing, monitoring, or automating work → Automation
- If it is still performing AI tasks → AI
- If it is primarily serving endpoints and business logic → APIs
- If it is a reusable package → Libraries
- If it is a user-facing application → Web, Mobile, or Desktop
- If it is analyzing existing software or systems → ReverseEngineering

Classify by the project's core purpose, not by its implementation details.
