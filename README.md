# AWS Bedrock RAG Knowledge Assistant

A Retrieval-Augmented Generation (RAG) application that uses Amazon Bedrock and Amazon S3 to answer questions from custom enterprise-policy documents.

## Project Overview

This project demonstrates an AWS-native RAG workflow for retrieving relevant information from documents and generating context-grounded responses with source citations.

## Architecture

User Question
    |
    v
Python Application / boto3
    |
    v
Amazon Bedrock Knowledge Base
    |
    v
Semantic Retrieval
    |
    v
Amazon S3 Documents
    |
    v
Amazon Bedrock Foundation Model
    |
    v
Grounded Answer + Source Citations

## AWS Services

- Amazon Bedrock
- Amazon S3
- Bedrock Knowledge Bases
- Amazon Titan Text Embeddings V2
- Amazon S3 Vectors
- AWS IAM

## Technologies

- Python
- boto3
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Embeddings

## Knowledge Base Documents

The sample knowledge base contains fictional enterprise documents covering:

- Employee benefits
- Vacation and leave policies
- IT support procedures

## Example Questions

- How many vacation days do employees receive?
- When do employee benefits begin?
- How should critical security incidents be reported?

## Features

- Document ingestion through Amazon S3
- Semantic vector retrieval
- Retrieval-Augmented Generation
- Source-grounded responses
- S3 source citations
- Amazon Bedrock foundation model integration

## Project Status

AWS infrastructure setup and RAG integration in progress.

## Background

Developed as a customized AWS Bedrock RAG implementation using AWS reference examples as a starting point.