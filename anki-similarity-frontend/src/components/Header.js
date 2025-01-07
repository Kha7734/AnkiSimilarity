import {AppBar, IconButton, Toolbar, Typography} from "@mui/material";
import {AccountCircle} from "@mui/icons-material";

const Header = () => {
  return (
    <AppBar position="fixed" sx={{ width: "100%", zIndex: 1201 }}>
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Vocabulary App
        </Typography>
        <IconButton color="inherit">
          <AccountCircle />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Header;