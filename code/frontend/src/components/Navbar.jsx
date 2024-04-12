import { Mail, Notifications, Pets } from "@mui/icons-material";
import {
  AppBar,
  Avatar,
  Badge,
  Box,
  InputBase,
  Menu,
  MenuItem,
  styled,
  Toolbar,
  Typography,
  Button
} from "@mui/material";
import React, { useState } from "react";



const StyledToolbar = styled(Toolbar)({
  display: "flex",
  justifyContent: "space-between",
});

const Search = styled("div")(({ theme }) => ({
  backgroundColor: "white",
  padding: "0 10px",
  borderRadius: theme.shape.borderRadius,
  width: "40%",
}));

const Icons = styled(Box)(({ theme }) => ({
  display: "none",
  alignItems: "center",
  gap: "20px",
  [theme.breakpoints.up("sm")]: {
    display: "flex",
  },
}));

const UserBox = styled(Box)(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  gap: "10px",
  [theme.breakpoints.up("sm")]: {
    display: "none",
  },
}));


const Navbar = () => {
  const [open, setOpen] = useState(false);
  const [resumeSearch, setResumeSearch] = useState(false);
  const [jobSearch, setJobSearch] = useState(false);

  const handleResumeClick = () =>{
  setResumeSearch(true)
  console.log(resumeSearch)
  }

  const handleJobClick = () =>{
  setJobSearch(true)
  console.log(jobSearch)
  }

  return (
    <AppBar position="sticky" >
      <StyledToolbar>
      </StyledToolbar>

     
    </AppBar>
  );
};

export default Navbar;
