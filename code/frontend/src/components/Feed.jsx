import {
  Box,
  Stack,
  Skeleton,
  InputBase,
  styled,
  Paper,
  IconButton,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import React, { useState, useEffect } from "react";
import Post from "./Post";
import axios from "axios";
import Typography from "@mui/material/Typography";

const Feed = (props) => {
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState(
    props.category == "job" ? "job" : "resume"
  );
  const [searchText, setSearchText] = useState("");
  const [responseData, setResponseData] = useState([{}]);
  const [searchData, setSearchData] = useState(false);
  const responseMockData = {
    predictions: [
      {
        id: "10001727",
        path: "https://storage.googleapis.com/download/storage/v1/b/hackathontestdata2024/o/10001727.pdf?generation=1710176879953629&alt=media",
        score: 0.9172105015039876,
      },
      {
        id: "10005171",
        path: "https://storage.googleapis.com/download/storage/v1/b/hackathontestdata2024/o/10005171.pdf?generation=1710176880349344&alt=media",
        score: 0.8517969968876015,
      },
      {
        id: "10030015",
        path: "https://storage.googleapis.com/download/storage/v1/b/hackathontestdata2024/o/10030015.pdf?generation=1710176881648615&alt=media",
        score: 1.0,
      },
      {
        id: "10041713",
        path: "https://storage.googleapis.com/download/storage/v1/b/hackathontestdata2024/o/10041713.pdf?generation=1710176882049870&alt=media",
        score: 0.9638904016267447,
      },
    ],
  };

  const submitRequest = () => {
    console.log(searchText);
    setLoading(true);
    setSearchData(true);

    const requestHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "3600",
    };

    let resumeRequest = {
      context: searchText,
      category: category,
      threshold: 0.7,
      noOfmatches: 50,
      inputPath:
        category === "resume"
          ? "https://console.cloud.google.com/storage/browser/hackathontestdata2024"
          : "https://console.cloud.google.com/storage/browser/hackathon1415",
    };

    const fetchData = axios
      .post(
        "https://us-central1-wellsfargo-genai24-8049.cloudfunctions.net/resumematching-api",
        resumeRequest,
        { headers: requestHeaders }
      )
      .then((res) => {
        setLoading(false);
        setResponseData(res.data.predictions);
      })
      .catch((e) => console.log(e));
  };

  const handlekeyDownEvent = (event) => {
    if (event.key === "Enter") {
      console.log("enter press here! ");
    }
  };

  const submitRequestData = (e) => {
    setSearchText(e.target.value);
  };

  const Search = styled("div")(({ theme }) => ({
    backgroundColor: "white",
    padding: "0 50px",
    borderRadius: theme.shape.borderRadius,
    borderBlockColor: "orange",
    width: "40%",
  }));
  return (
    <Box flex={4} p={{ xs: 0, md: 2 }}>
      <Typography variant="h6" gutterBottom>
        {category == "job" ? "Find Jobs" : "Find Resumes"}
      </Typography>

      <Paper
        component="form"
        sx={{
          p: "2px 2px",
          display: "flex",
          alignItems: "center",
          width: 800,
          margin: "auto",
        }}
      >
        <InputBase
          sx={{ ml: 8, flex: 1 }}
          placeholder={category == "job" ? "Search Jobs" : "Search Resumes"}
          value={searchText}
          onChange={submitRequestData}
        />
        <IconButton
          type="button"
          sx={{ p: "10px" }}
          value={searchText}
          onClick={submitRequest}
          aria-label="search"
        >
          <SearchIcon />
        </IconButton>
      </Paper>
      {loading ? (
        <Stack spacing={1}>
          <Skeleton variant="text" height={100} />
          <Skeleton variant="text" height={20} />
          <Skeleton variant="text" height={20} />
          <Skeleton variant="rectangular" height={300} />
        </Stack>
      ) : searchData && responseData.length > 0 ? (
        <>
          {responseData.map((data) => (
            <Post ids={data.id} path={data.path} score={data.score}></Post>
          ))}
        </>
      ) : (
        <div align="center" m={40} p={40} mb={40}>
          <Typography variant="h1" gutterBottom></Typography>
          <label> No Data Found</label>
        </div>
      )}
    </Box>
  );
};

export default Feed;
