# 🏦 Bank System Database Simulation

A comprehensive and user-friendly bank system simulation designed using Python and SQL Server as the final project for Database Design course.

## 📋 About The Project

> **Final Project of Database Design Principles**  
> Under The Supervision of [Dr. Zahra Pourbahman](https://scholar.google.com/citations?user=CCw-ockAAAAJ&hl=en)  
> Fall 2023 - Amir Kabir University Of Technology

This project implements a complete banking system with secure user authentication, multiple account management, and three different transaction methods while adhering to banking regulations and daily transfer limits.

## 🛠️ Tech Stack

* **Database**: SQL Server
* **Backend**: Python 3.x
* **Additional Libraries**: pyodbc, datetime, hashlib

## ✨ Key Features

### 🔐 User Management
- ✅ Secure user registration with unique national code and username validation
- ✅ Password hashing using SHA-256 for enhanced security
- ✅ User authentication and session management

### 💳 Account Management
- ✅ Create multiple bank accounts per user
- ✅ Generate unique card numbers and Sheba numbers for each account
- ✅ View all accounts associated with a user

### 💸 Transaction System
- ✅ **Card-to-Card transfers** with daily limit of 10 million Tomans
- ✅ **SATNA transfers** to destination Sheba numbers with daily limits
- ✅ **PAYA transfers** to destination Sheba numbers with daily limits
- ✅ Comprehensive transaction history tracking
- ✅ Unique tracking codes for all transactions

### 📊 Transaction History
- ✅ View last N transactions for any account
- ✅ Verify transaction validity using tracking codes
- ✅ Access control (users can only see their own transactions)

## 🗂️ Database Schema

The database includes the following tables with proper relationships:

- **Users** 👥 (UserID, FirstName, LastName, NationalCode, Username, PasswordHash)
- **Accounts** 💳 (AccountID, UserID, CardNumber, ShebaNumber, Balance)
- **Transactions** 🔄 (TransactionID, SourceAccountID, DestinationAccountID, Amount, Type, Status, DateTime, TrackingCode)
- **DailyLimits** ⚖️ (LimitID, AccountID, TransactionType, DailyAmount, Date)

## 🚀 How To Run

1. **Prerequisites**: Ensure you have SQL Server installed and running
2. **Database Setup**: Execute the provided SQL script to create the database and tables
3. **Install Dependencies**: `pip install pyodbc`
4. **Run Application**: Execute the Python script and follow the menu prompts

## 📸 Preview

### 1. Startup Menu 🏠
![Startup Menu](https://github.com/Amirbehnam1009/Bank-System-Database-Simulation-/assets/117163007/86fa3939-1471-44fb-922d-0955f700b7d3)

### 2. Dashboard After Login 📋
![Dashboard](https://github.com/Amirbehnam1009/Bank-System-Database-Simulation-/assets/117163007/f7478060-046c-4a42-a467-83c596b4c39e)

### 3. Transaction Simulation 🔄
![Transaction](https://github.com/Amirbehnam1009/Bank-System-Database-Simulation-/assets/117163007/858e580d-abcd-45aa-abe9-bf214604a4b1)

## 🎯 Advanced Features

- **Triggers** ⚡: Implemented for maintaining transaction integrity and updating balances
- **Input Validation** 🛡️: Comprehensive validation for all user inputs
- **Error Handling** ❌: Graceful error handling with user-friendly messages
- **Daily Limit Enforcement** 📅: Automatic reset of daily limits at midnight
