import {List, ListItem, ListItemText} from "@mui/material";
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <div style={{ width: "240px", position: "fixed", height: "100vh", backgroundColor: "#f5f5f5" }}>
      <List>
        <ListItem button component={Link} to="/vocabulary">
          <ListItemText primary="Vocabulary" />
        </ListItem>
        <ListItem button component={Link} to="/datasets">
          <ListItemText primary="Datasets" />
        </ListItem>
        <ListItem button component={Link} to="/progress">
          <ListItemText primary="Progress" />
        </ListItem>
        <ListItem button component={Link} to="/settings">
          <ListItemText primary="Settings" />
        </ListItem>
      </List>
    </div>
  );
};

export default Sidebar;