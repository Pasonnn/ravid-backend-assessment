# Business Requirements Document

## Project

- Project name: R.A.V.I.D. Backend Assessment
- Assessment title: Assessment & Evaluation for Remote Candidates - Apr 2026
- Assessment type: take-home backend exercise

## Background

The assessment asks for a Python backend system that can:

- upload CSV files
- run CSV processing operations asynchronously
- expose task status and processed output
- support user registration and login
- provide centralized structured logging and visualization
- run through Docker and Docker Compose

This work is intended to demonstrate backend engineering ability across API design, async processing, observability, and delivery readiness.

## Objective

Deliver a clean, working backend that satisfies the assessment requirements and is easy for reviewers to run, inspect, and evaluate.

## Stakeholders

- Candidate: implements and documents the solution
- Reviewers: backend engineers and stakeholders evaluating technical quality
- End users in the assessment context: authenticated users uploading CSV files and requesting processing operations

## Business Goals

- Demonstrate practical backend implementation skills
- Show clean API and async task design
- Show production-minded observability and containerized delivery
- Provide submission artifacts that minimize reviewer setup effort

## In Scope

- CSV upload API
- CSV processing API
- task status API
- authenticated processed file download endpoint
- user registration and login
- JWT-protected routes
- background task execution using Celery and Redis
- structured logging with Django and Celery
- Loki and Grafana-based log aggregation and visualization
- Docker Compose setup for the required services
- README and API documentation

## Out Of Scope

- frontend application beyond what is necessary for API demonstration
- advanced user roles and permissions beyond protected versus public routes
- multi-tenant behavior
- production cloud deployment
- large-scale operational hardening beyond what is reasonable for a take-home exercise

## Primary Users And Core Journeys

### Authenticated User

- registers an account
- logs in
- uploads a CSV file
- starts a processing operation
- checks task progress
- inspects output preview and file link

### Reviewer

- reads README
- runs Docker Compose
- exercises APIs from the provided documentation
- verifies logs and dashboard behavior

## Deliverables

- working backend codebase
- Docker Compose stack
- API documentation
- README with setup and run instructions
- structured logging pipeline and Grafana dashboard

## Success Criteria

- required endpoints behave as specified
- protected endpoints require JWT auth
- CSV operations run asynchronously
- task status exposes success and failure clearly
- logs are structured and visible in Grafana
- the project can be run from documented Docker commands

## Constraints

- short delivery timeline
- backend-focused assessment
- exact endpoint names from the brief should be preserved
- assessment includes ambiguous areas that must be documented as explicit defaults

## Risks

- ambiguous auth contract in the brief
- ambiguous filter request schema
- delivery artifacts left too late
- observability setup complexity relative to time box

## Working Principle

Where the assessment is unclear, the implementation should choose a pragmatic default, document it, and keep the reviewer experience simple.
