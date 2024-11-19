from graphviz import Digraph

# Create a Digraph object to visualize user journeys
diagram = Digraph(name="User Journeys for AI Model Access Web Application", format="png")
diagram.attr(rankdir="LR", size='10,10')

# Define nodes and subgraphs for each journey

# --- Journey 1: Registration & Authentication ---
# Registration
diagram.node("Start", "Start (Landing Page)")
diagram.node("SignUp", "User Registration")
diagram.node("LoginPage", "Login Page")
diagram.node("Credentials", "Enter Credentials")
diagram.node("Verify", "Verify Credentials")
diagram.node("LoginSuccess", "Login Success (Home Page)")
diagram.node("SessionStart", "Start Session")

# Define edges for Registration & Authentication
diagram.edge("Start", "SignUp", label="New User")
diagram.edge("SignUp", "LoginPage", label="Account Created")
diagram.edge("Start", "LoginPage", label="Returning User")
diagram.edge("LoginPage", "Credentials", label="Login Clicked")
diagram.edge("Credentials", "Verify")
diagram.edge("Verify", "LoginSuccess", label="Valid")
diagram.edge("Verify", "LoginPage", label="Invalid (Retry)")
diagram.edge("LoginSuccess", "SessionStart", label="Session Created")

# --- Journey 2: Model Access ---
# Model Access Process
diagram.node("ModelList", "Access Model List")
diagram.node("SelectModel", "Select Model (Whisper, Llama 3, RAG)")
diagram.node("CheckAccess", "Check Access Rights")
diagram.node("AccessDenied", "Access Denied")
diagram.node("InputRequest", "Enter Request for Model")
diagram.node("ProcessRequest", "Process Request")
diagram.node("DisplayResult", "Display Result")

# Define edges for Model Access
diagram.edge("SessionStart", "ModelList")
diagram.edge("ModelList", "SelectModel")
diagram.edge("SelectModel", "CheckAccess")
diagram.edge("CheckAccess", "AccessDenied", label="No Access")
diagram.edge("CheckAccess", "InputRequest", label="Access Granted")
diagram.edge("InputRequest", "ProcessRequest")
diagram.edge("ProcessRequest", "DisplayResult")

# --- Journey 3: Admin Management ---
# Admin Management
diagram.node("AdminLogin", "Admin Login (Home)")
diagram.node("CreateUser", "Create User Account")
diagram.node("ManageAccess", "Manage Model Access")
diagram.node("EditUser", "Edit/Delete User Account")

# Define edges for Admin Management
diagram.edge("LoginSuccess", "AdminLogin", label="Admin Role")
diagram.edge("AdminLogin", "CreateUser")
diagram.edge("AdminLogin", "ManageAccess")
diagram.edge("AdminLogin", "EditUser")

# --- Journey 4: Logout Process ---
# Logout
diagram.node("Logout", "Logout")
diagram.node("EndSession", "End Session")
diagram.node("Redirect", "Redirect to Login Page")

# Define edges for Logout Process
diagram.edge("LoginSuccess", "Logout", label="Logout Clicked")
diagram.edge("Logout", "EndSession")
diagram.edge("EndSession", "Redirect")

# Render the diagram
diagram.render('/mnt/data/User_Journeys_Diagram')
'/mnt/data/User_Journeys_Diagram.png'
