import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  LinearProgress,
} from "@mui/material";
import { Link } from "react-router-dom";
import Header from "../components/Header"; // Ensure Header is imported
import Sidebar from "../components/Sidebar";
import { useAuth } from "../AuthContext";

const Dashboard = () => {
  const [progress, setProgress] = useState(0);
  const [recentActivity, setRecentActivity] = useState([]);
  const [datasets, setDatasets] = useState([]);
  const [userProgress, setUserProgress] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    const fetchData = async () => {
      if (!user) return;

      try {
        const progressResponse = await axios.get(`/api/progress/user/${user._id}`);
        setUserProgress(progressResponse.data);

        const totalCards = progressResponse.data.length;
        const completedCards = progressResponse.data.filter(
          (p) => p.status === "completed"
        ).length;
        const progressPercentage = totalCards > 0 ? (completedCards / totalCards) * 100 : 0;
        setProgress(progressPercentage);

        // const activityResponse = await axios.get("/vocabulary/recent", {
        //   params: { user_id: user.user_id },
        // });
        // setRecentActivity(activityResponse.data);
        //
        // const datasetsResponse = await axios.get("/datasets", {
        //   params: { user_id: user.user_id },
        // });
        // setDatasets(datasetsResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [user]);

  return (
    <div>
      <Header /> {/* Include Header */}
      <Sidebar />
      <Container sx={{ marginLeft: "240px", marginTop: "64px", padding: "12px" }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Grid container spacing={3}>
          {/* Progress Overview */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Progress Overview
                </Typography>
                <LinearProgress variant="determinate" value={progress} />
                <Typography variant="body1" sx={{ mt: 2 }}>
                  {progress.toFixed(2)}% of your vocabulary mastered
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                  {userProgress.filter((p) => p.status === "completed").length} /{" "}
                  {userProgress.length} cards completed
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Recent Activity */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Recent Activity
                </Typography>
                <List>
                  {recentActivity.map((activity, index) => (
                    <ListItem key={index}>
                      {activity.action} "{activity.word}" on {activity.date}
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Datasets Overview */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Your Datasets
                </Typography>
                <Button
                  variant="contained"
                  color="primary"
                  component={Link}
                  to="/datasets"
                >
                  Create New Dataset
                </Button>
                <List>
                  {datasets.map((dataset, index) => (
                    <ListItem key={index}>
                      {dataset.name} ({dataset.cardCount} cards)
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* User Progress Details */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Your Progress Details
                </Typography>
                <List>
                  {userProgress.map((progress, index) => (
                    <ListItem key={index}>
                      <Typography variant="body1">
                        <strong>Card ID:</strong> {progress.card_id}
                      </Typography>
                      <Typography variant="body1">
                        <strong>Status:</strong> {progress.status}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        <strong>Last Reviewed:</strong>{" "}
                        {progress.last_reviewed || "Never"}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        <strong>Next Review:</strong>{" "}
                        {progress.next_review || "Not scheduled"}
                      </Typography>
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
};

export default Dashboard;