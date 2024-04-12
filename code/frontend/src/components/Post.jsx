import {
  Favorite,
  FavoriteBorder,
  MoreVert,
  Share,
  Download,
  Visibility,
} from "@mui/icons-material";
import {
  Avatar,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  CardMedia,
  Checkbox,
  Box,
  IconButton,
  Typography,
} from "@mui/material";

const Post = (props) => {
  const downloadFile = function () {
    //let fileURL ='http://localhost:3000/resume-icon.png';
    let fileURL = props.path;
    const fileName = fileURL.split("/").pop();
    const aTag = document.createElement("a");
    aTag.href = fileURL;
    aTag.setAttribute("download", fileName);
    document.body.appendChild(aTag);
    aTag.click();
    aTag.remove();
  };
  return (
    <Card sx={{ margin: 5 }}>
      <CardHeader
        avatar={
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: 1,
              alignItems: "center",
              bgcolor: "primary.main",
            }}
          >
            <Typography variant="h6" gutterBottom sx={{ color: "white" }}>
              {(Math.round(props.score * 100) / 100).toFixed(2)}
            </Typography>
          </Box>
        }
        action={
          <div>
            <IconButton aria-label="visibility">
              <Visibility />
            </IconButton>
            <IconButton aria-label="download" onClick={downloadFile}>
              <Download onClick={downloadFile} />
            </IconButton>
          </div>
        }
        subheader={props.ids}
      />
      {/* <CardMedia
        component="img"
        height="20%"
        image={props.path}
        alt="Paella dish"
      />
      
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          This impressive paella is a perfect party dish and a fun meal to cook
          together with your guests. Add 1 cup of frozen peas along with the
          mussels, if you like.
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <IconButton aria-label="add to favorites">
          <Checkbox
            icon={<FavoriteBorder />}
            checkedIcon={<Favorite sx={{ color: "red" }} />}
          />
        </IconButton>
        <IconButton aria-label="share">
          <Share />
        </IconButton>
      </CardActions>*/}
    </Card>
  );
};

export default Post;
