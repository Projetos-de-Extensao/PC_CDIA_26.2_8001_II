# AWS Resource Dashboard for University Course Management

## Project Overview
This proof of concept (POC) aims to create a dashboard that allows university professors to manage AWS resources for their courses throughout a semester. The system will enable professors to create, monitor, block, and terminate AWS resources for their respective classes.

## System Architecture
- **Frontend**: Web-based dashboard using React.js
- **Backend**: Python com Django Rest Framework
- **Authentication**: AWS Cognito for user management
- **Database**: MongoDB for storing course and resource data
- **AWS Integration**: AWS SDK for resource management

## Key Features
1. **Professor Authentication**
   - Secure login through AWS Cognito
   - Role-based access control (Professor vs Admin)

2. **Course Management**
   - Create new courses with semester details
   - Associate professors with specific courses
   - View enrolled students per course

3. **Resource Control**
   - Provision AWS resources (EC2 instances, S3 buckets)
   - Monitor resource usage and costs
   - Pause/block resource allocation
   - Terminate resources when semester ends

4. **Dashboard Components**
   - Resource utilization charts
   - Cost tracking dashboard
   - Course progress monitoring
   - Alert system for resource thresholds

## Implementation Steps
1. Set up AWS Cognito user pool for authentication
2. Create database schema for courses and resources
3. Implement AWS SDK integration for resource management
4. Develop frontend UI components
5. Build REST API endpoints
6. Test resource provisioning and termination workflows

## Technical Requirements
- Node.js version 16+
- AWS CLI configured with appropriate permissions
- MongoDB instance running
- Python 3.8+ with Django and Django Rest Framework
- React.js development environment
 
## Security Considerations
- Role-based access control for professors
- Resource usage limits per course
- Audit logging for all resource operations
- Secure API endpoints with authentication middleware

---

## First Steps
1. **Project Setup and Environment Configuration**
   - Initialize Python project with Django framework
   - Set up development environment with necessary dependencies (Django, Django Rest Framework, etc.)
   - Configure MongoDB connection and create initial database schema
   - Install and configure AWS SDK for Python
   - Set up development database with sample data

2. **Authentication Implementation**
   - Create AWS Cognito user pool and identity pool
   - Implement authentication middleware using AWS Cognito
   - Set up role-based access control (RBAC) system
   - Create login/logout functionality with session management

3. **Database Design and Schema Creation**
   - Design MongoDB schemas for users, courses, resources, and audit logs
   - Create initial database structure with proper indexing
   - Implement data models for professors, students, and course associations
   - Set up database connection utilities and configuration files

4. **Frontend Foundation**
   - Initialize React.js application with required dependencies
   - Set up routing system (React Router)
   - Create basic UI components structure
   - Configure development server and build tools

5. **API Endpoint Planning**
   - Plan REST API endpoints for courses, resources, and user management
   - Define request/response formats for all endpoints
   - Design authentication and authorization middleware
   - Set up initial API routes and controllers

6. **AWS Integration Setup**
   - Configure AWS credentials with appropriate IAM roles and permissions
   - Implement basic AWS SDK configurations for EC2 and S3 services
   - Create initial resource management functions (create, list, terminate)
   - Set up cost monitoring and tracking mechanisms</START EDITING HERE>

---

## Functional Requirements
1. **User Management**
   - Professors can authenticate using AWS Cognito
   - System supports role-based access control (Professor, Admin)
   - Admin users can manage professor accounts

2. **Course Management**
   - Professors can create new courses with semester and academic year information
   - Professors can associate themselves with existing courses
   - System displays enrolled students per course
   - Course data includes name, description, semester, academic year, associated professor

3. **Resource Provisioning**
   - Professors can request creation of AWS resources (EC2 instances, S3 buckets)
   - System provisions resources within defined constraints
   - Resource details include type, status, creation date, owner

4. **Resource Monitoring**
   - Dashboard displays real-time resource utilization metrics
   - Cost tracking dashboard shows expenses per course and overall
   - Alerts triggered when resource usage exceeds predefined thresholds

5. **Resource Control**
   - Professors can pause/block resource allocation
   - Professors can terminate resources manually
   - System automatically terminates all resources at end of semester
   - Resource state changes are logged with timestamps

6. **Reporting and Analytics**
   - Dashboard provides visual charts for resource usage
   - Cost analytics by course and time period
   - Audit logs for all resource operations

## Non-Functional Requirements
1. **Performance**
   - Dashboard loads within 3 seconds
   - Resource monitoring updates every 5 minutes
   - API response times under 2 seconds

2. **Security**
   - All API endpoints protected with authentication middleware
   - Role-based access control enforced for all operations
   - Audit logs maintained for all resource changes
   - Secure storage of AWS credentials using IAM roles

3. **Scalability**
   - System supports concurrent usage by multiple professors
   - Database queries optimized with proper indexing
   - Resource provisioning scales with demand

4. **Usability**
   - Intuitive dashboard UI with clear navigation
   - Responsive design for desktop and mobile access
   - Clear error messages and user guidance

5. **Reliability**
   - System uptime of 99.5%
   - Automatic failover mechanisms for critical services
   - Data backup and recovery procedures in place

## Business Rules
1. **Course Management Rules**
   - Each course must have a unique name within a semester
   - Only one professor can be associated with a course
   - Courses cannot be created for past semesters
   - Students are automatically enrolled when added to course

2. **Resource Management Rules**
   - Resources must be associated with an active course
   - Professors can only manage resources in courses they own
   - Resource creation is limited by predefined quotas per course
   - All resource operations must be logged for audit purposes

3. **Access Control Rules**
   - Admin users have full access to all courses and resources
   - Regular professors can only access their assigned courses
   - Resource termination requires explicit confirmation
   - Access logs are maintained for all user activities

4. **Cost Management Rules**
   - Cost tracking is enabled per course
   - Alerts are triggered when costs exceed 80% of budget
   - Monthly cost reports are generated automatically
   - Resources are automatically terminated if budget is exceeded

5. **System Lifecycle Rules**
   - Resources are automatically terminated at end of academic semester
   - System validates resource status before any operation
   - All operations must have timestamp and user context
   - Backup procedures run daily for critical data