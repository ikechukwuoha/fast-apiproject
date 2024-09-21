# database/db.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

# Create a Motor client and connect to the MongoDB database
client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DATABASE_NAME]



# List of default permissions
# Default permissions list (as defined in your previous message)
default_permissions = [
    # Resource Management
    {"name": "Read", "description": "Allows viewing of resources"},
    {"name": "Create", "description": "Allows creation of new resources"},
    {"name": "Edit", "description": "Allows editing of existing resources"},
    {"name": "Delete", "description": "Allows deletion of resources"},
    {"name": "Archive Resources", "description": "Allows archiving of resources"},
    {"name": "Restore Resources", "description": "Allows restoring of archived resources"},
    # User Management
    {"name": "Manage Users", "description": "Allows management of users"},
    {"name": "Add Users", "description": "Allows adding new users"},
    {"name": "Edit User Roles", "description": "Allows editing of user roles"},
    {"name": "Reset User Passwords", "description": "Allows resetting of user passwords"},
    {"name": "Deactivate Users", "description": "Allows deactivation of users"},
    {"name": "Reactivate Users", "description": "Allows reactivation of deactivated users"},
    # Role Management
    {"name": "Manage Roles", "description": "Allows management of roles"},
    {"name": "Create Roles", "description": "Allows creation of new roles"},
    {"name": "Edit Role Permissions", "description": "Allows editing of role permissions"},
    {"name": "Delete Roles", "description": "Allows deletion of roles"},
    {"name": "Assign Roles", "description": "Allows assigning roles to users"},
    # Admin Dashboard
    {"name": "Access Admin Dashboard", "description": "Grants access to admin features"},
    {"name": "View System Logs", "description": "Allows viewing of system logs"},
    {"name": "Manage System Settings", "description": "Allows management of system settings"},
    {"name": "View Admin Notifications", "description": "Allows viewing of admin notifications"},
    # Analytics and Reporting
    {"name": "View Analytics", "description": "Allows viewing of analytics"},
    {"name": "Generate Reports", "description": "Allows generation of reports"},
    {"name": "Export Data", "description": "Allows exporting of data"},
    {"name": "Schedule Reports", "description": "Allows scheduling of report generation"},
    # Security and Compliance
    {"name": "Manage Security Policies", "description": "Allows management of security policies"},
    {"name": "View Audit Trails", "description": "Allows viewing of audit trails"},
    {"name": "Manage Compliance", "description": "Allows management of compliance"},
    {"name": "Audit User Activity", "description": "Allows auditing of user activity"},
    {"name": "Manage Data Retention", "description": "Allows management of data retention policies"}
]

# Extend with new permissions
default_permissions.extend([
    # Content Management
    {"name": "Moderate Content", "description": "Allows moderation of user-generated content"},
    {"name": "Approve Posts", "description": "Allows approval of posts before they are visible"},
    {"name": "Reject Posts", "description": "Allows rejection of posts"},
    {"name": "Feature Posts", "description": "Allows marking posts as featured"},
    {"name": "Publish Content", "description": "Allows publishing drafted content"},
    {"name": "Unpublish Content", "description": "Allows unpublishing of content"},
    # API and Integration Management
    {"name": "Manage API Access", "description": "Allows managing access to system APIs"},
    {"name": "Create API Keys", "description": "Allows creating new API keys"},
    {"name": "Revoke API Keys", "description": "Allows revoking existing API keys"},
    {"name": "View API Usage", "description": "Allows viewing API access logs and statistics"},
    {"name": "Manage Webhooks", "description": "Allows managing system webhooks for integrations"},
    # System Administration
    {"name": "Perform System Backup", "description": "Allows performing system backups"},
    {"name": "Restore from Backup", "description": "Allows restoring the system from backups"},
    {"name": "Restart Services", "description": "Allows restarting system services"},
    {"name": "Perform System Maintenance", "description": "Allows performing system maintenance tasks"},
    {"name": "Manage Database", "description": "Allows managing the database and performing migrations"},
    # Financial and Billing Management
    {"name": "View Billing Information", "description": "Allows viewing billing and payment details"},
    {"name": "Manage Billing Settings", "description": "Allows managing billing settings and payment methods"},
    {"name": "Process Payments", "description": "Allows processing payments and issuing refunds"},
    {"name": "Manage Subscriptions", "description": "Allows managing subscriptions"},
    {"name": "Issue Invoices", "description": "Allows issuing and managing invoices"},
    # Advanced User Management
    {"name": "Impersonate Users", "description": "Allows impersonation of users for troubleshooting"},
    {"name": "Ban Users", "description": "Allows permanently banning users"},
    {"name": "View User Activity Logs", "description": "Allows viewing user activity logs"},
    {"name": "Manage User Groups", "description": "Allows managing user groups or teams"},
    {"name": "Invite Users", "description": "Allows inviting new users to the platform"},
    # Notification and Messaging
    {"name": "Send Notifications", "description": "Allows sending system-wide notifications"},
    {"name": "Manage Notification Settings", "description": "Allows managing notification preferences"},
    {"name": "View User Messages", "description": "Allows viewing user messages"},
    {"name": "Delete User Messages", "description": "Allows deleting user messages"},
    # E-commerce and Product Management
    {"name": "Manage Products", "description": "Allows managing products in the system"},
    {"name": "Manage Orders", "description": "Allows viewing and managing customer orders"},
    {"name": "Refund Orders", "description": "Allows processing refunds for customer orders"},
    {"name": "Manage Discounts", "description": "Allows managing discounts and promotions"},
    {"name": "View Sales Reports", "description": "Allows viewing sales reports and statistics"},
    # Audit and Compliance
    {"name": "Audit System Changes", "description": "Allows auditing system changes"},
    {"name": "Generate Compliance Reports", "description": "Allows generating compliance reports"},
    {"name": "Manage Legal Policies", "description": "Allows managing system legal policies"},
    # File Management
    {"name": "Upload Files", "description": "Allows uploading files"},
    {"name": "Delete Files", "description": "Allows deleting files"},
    {"name": "View File Metadata", "description": "Allows viewing file metadata"},
    {"name": "Manage File Storage", "description": "Allows managing file storage settings"},
    # Feature Management
    {"name": "Manage Feature Flags", "description": "Allows managing feature flags"},
    {"name": "Beta Test Features", "description": "Allows testing beta features"},
    # Localization Management
    {"name": "Manage Translations", "description": "Allows managing system translations"},
    {"name": "Add New Languages", "description": "Allows adding new languages to the system"},
    {"name": "Edit Language Files", "description": "Allows editing language translation files"}
])






# Access the users collection
"""DATABASE TO STORE USERS"""
users_collection = database["users"]

"""DATABASE TO STORE ADMIN USERS"""
admin_users_collection = database["admin_user"]

"""DATABASE TO STORE ROLES, GROUPS AND PERMISSIONS"""
groups_collection = database["groups"]
roles_collection = database["roles"]
permissions_collection = database["permissions"]


