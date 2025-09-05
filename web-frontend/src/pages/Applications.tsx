/**
 * Page displaying a list of applications.
 * Includes a header and a button to navigate to the application creation page.
 */

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
import { useCallback } from "react";

export const ApplicationsPage: React.FC = () => {
  const navigate = useNavigate();

  // Memoized navigation handler for performance
  const handleCreateClick = useCallback(() => {
    navigate("/apps/create");
  }, [navigate]);

  return (
    <Box width="100%" height="100svh">
      <Container maxWidth="5xl" py="10">
        <Flex>
          <Heading size="4xl" letterSpacing="tight">
            Projects
          </Heading>
          <Spacer />
          <Button
            onClick={handleCreateClick}
            size="md"
            variant="solid"
            colorScheme="cyan"
            aria-label="Add a new application"
          >
            <FiPlus /> Add a New Application
          </Button>
        </Flex>
      </Container>
    </Box>
  );
};
