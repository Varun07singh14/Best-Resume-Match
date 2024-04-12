import React from "react";
import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";
import { Box } from "@mui/material";

function Home(props) {
  const navigate = useNavigate();
  const handleResumeClick = () => {
    navigate("/resumes");
  };

  const handleJobsClick = () => {
    navigate("/jobs");
  };
  return (
    <Box sx={{ display: "flex", justifyContent: "center" }}>
      <Button
        variant="contained"
        onClick={handleJobsClick}
        sx={{ margin: "20px" }}
      >
        Find Jobs
      </Button>
      <Button
        variant="contained"
        onClick={handleResumeClick}
        sx={{ margin: "20px" }}
      >
        Find Resumes
      </Button>
    </Box>
  );
}

export default Home;
