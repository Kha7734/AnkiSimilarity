import React from "react";
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import ProtectedRoute from "./services/ProtectedRoute";
import Layout from "./components/Layout"; // Import the Layout component
import Dashboard from "./pages/Dashboard";
import Vocabulary from "./pages/Vocabulary";
import Datasets from "./pages/Datasets";
import Progress from "./pages/Progress";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import Register from "./pages/Register";
import {AuthProvider} from "./AuthContext";

function App() {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    {/* Routes with Layout */}
                    <Route element={<ProtectedRoute/>}>
                        <Route element={<Layout/>}>
                            <Route path="/" element={<Dashboard/>}/>
                            <Route path="/dashboard" element={<Dashboard/>}/>
                            <Route path="/vocabulary" element={<Vocabulary/>}/>
                            <Route path="/datasets" element={<Datasets/>}/>
                            <Route path="/progress" element={<Progress/>}/>
                            <Route path="/settings" element={<Settings/>}/>
                        </Route>
                    </Route>

                    {/* Routes without Layout */}
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/register" element={<Register/>}/>
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;