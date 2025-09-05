/**
 * Form component for creating a new application.
 * Includes fields for application name and runtime selection.
 */

import { isEmptyString } from "@/util";
import {
  Box,
  Button,
  Container,
  Field,
  Heading,
  Icon,
  Input,
  Portal,
  Select,
  Span,
  Text,
  type ListCollection,
} from "@chakra-ui/react";
import type { IconType } from "react-icons";
import { FaPython } from "react-icons/fa6";

interface CreateAppFormProps {
  appName: string;
  setAppName: (name: string) => void;
  runtimeSelect: string[];
  setRuntimeSelect: (runtimes: string[]) => void;
  gitRepo: string;
  setGitRepo: (url: string) => void;
  runtimeList: ListCollection<{
    label: string;
    icon: string;
    value: string;
  }>;
  onSubmit: () => void;
}

// Maps runtime language to corresponding icon
const iconsMap: Record<string, IconType> = {
  Python: FaPython,
};

export const CreateAppForm: React.FC<CreateAppFormProps> = ({
  appName,
  setAppName,
  runtimeSelect,
  setRuntimeSelect,
  runtimeList,
  onSubmit,
  gitRepo, setGitRepo
}) => {
  return (
    <Box width="100%" height="100svh">
      <Container maxWidth="5xl" py="10" height="100%" width="100%">
        <Heading size="4xl" letterSpacing="tight">
          Create a New Application
        </Heading>

        <Box my="10">
          {/* Application name input */}
          <Field.Root maxW="36rem" my="5" required>
            <Field.Label>
              Application Name
              <Text as="span" color="red.500" ml="1">
                *
              </Text>
            </Field.Label>
            <Input
              value={appName}
              onChange={(e) => setAppName(e.target.value)}
              placeholder="Python-app-1"
              width="400px"
            />
          </Field.Root>

          {/* Runtime selection dropdown */}
          <Select.Root
            value={runtimeSelect}
            onValueChange={(e) => setRuntimeSelect(e.value)}
            collection={runtimeList}
            size="sm"
            width="320px"
            my="5"
            required
          >
            <Select.HiddenSelect />
            <Select.Label>
              Select framework
              <Text as="span" color="red.500" ml="1">
                *
              </Text>
            </Select.Label>
            <Select.Control>
              <Select.Trigger>
                <Select.ValueText placeholder="Select framework" />
              </Select.Trigger>
              <Select.IndicatorGroup>
                <Select.Indicator />
              </Select.IndicatorGroup>
            </Select.Control>

            <Portal>
              <Select.Positioner>
                <Select.Content>
                  {runtimeList.items.map((runtime) => {
                    const IconComponent = iconsMap[runtime.icon];
                    return (
                      <Select.Item item={runtime} key={runtime.label}>
                        <Span>
                          <Icon mr="2">
                            {IconComponent ? <IconComponent /> : null}
                          </Icon>
                          {runtime.label}
                        </Span>
                        <Select.ItemIndicator />
                      </Select.Item>
                    );
                  })}
                </Select.Content>
              </Select.Positioner>
            </Portal>
          </Select.Root>

          <Field.Root maxW="36rem" my="5" required>
            <Field.Label>
              Git Repository URL
              <Text as="span" color="red.500" ml="1">
                *
              </Text>
            </Field.Label>
            <Input
              value={gitRepo}
              onChange={(e) => setGitRepo(e.target.value)}
              placeholder="https://github.com/ahnaf-zamil/stratus"
              width="400px"
            />
          </Field.Root>

          {/* Submit button */}
          <Button
            disabled={!runtimeSelect.length || isEmptyString(appName) || isEmptyString(gitRepo)}
            onClick={onSubmit}
            my="5"
          >
            Create Application
          </Button>
        </Box>
      </Container>
    </Box>
  );
};
