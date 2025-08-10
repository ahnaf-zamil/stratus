import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Spacer,
} from "@chakra-ui/react";
import type React from "react";
import { FiPlus } from "react-icons/fi";
import { useNavigate } from "react-router";

export const ApplicationsPage: React.FC = () => {
  const navigate = useNavigate();
  return (
    <Box width="100%" height="100svh">
      <Container maxWidth="5xl" paddingTop="10">
        <Flex>
          <Heading size="4xl" letterSpacing="tight">
            Projects
          </Heading>
          <Spacer />
          <Button
            onClick={() => {
              navigate("/apps/create");
            }}
            size="md"
            variant="solid"
            colorPalette="cyan"
          >
            <FiPlus /> Add a New Application
          </Button>
        </Flex>
      </Container>
    </Box>
  );
};
