import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../AuthContext"; // Assuming you have an AuthContext

const ProtectedRoute = () => {
  const { user } = useAuth(); // Get the user from your authentication context

  if (!user) {
    // Redirect to the login page if the user is not logged in
    return <Navigate to="/login" replace />;
  }

  // Render the protected route if the user is logged in
  return <Outlet />;
};

export default ProtectedRoute;