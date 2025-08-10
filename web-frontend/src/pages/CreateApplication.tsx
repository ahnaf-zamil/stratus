import { createApplication, getAppRuntimes } from "@/api/apps";
import type { IRuntime } from "@/api/interfaces";
import { isEmptyString } from "@/util";
import {
  Text,
  Box,
  Container,
  createListCollection,
  Field,
  Heading,
  Icon,
  Input,
  Portal,
  Select,
  Span,
  Button,
} from "@chakra-ui/react";
import type React from "react";
import { useEffect, useState } from "react";
import type { IconType } from "react-icons";
import { FaPython } from "react-icons/fa6";

const iconsMap: Record<string, IconType> = {
  Python: FaPython,
};

export const CreateApplicationPage: React.FC = () => {
  const [appName, setAppName] = useState<string>("");
  const [runtimeSelect, setRuntimeSelect] = useState<string[]>([]);

  const [runtimes, setRuntimes] = useState<IRuntime[]>([]);
  const runtimeList = createListCollection({
    items: runtimes.map((runtime) => ({
      label: `${runtime.name} ${runtime.version}`,
      icon: runtime.name,
      value: runtime.id,
    })),
  });

  useEffect(() => {
    getAppRuntimes().then(([data, error]) => {
      if (error) {
        // Handle error
      } else {
        setRuntimes(data!);
      }
    });
  }, []);

  const handleSubmit = async () => {
    const [resp, err] = await createApplication(appName, runtimeSelect[0]);
    if (err) {
      // Handle err
      console.log(err);
    } else {
      console.log(resp);
    }
  };

  return (
    <Box width="100%" height="100svh">
      <Container maxWidth="5xl" paddingTop="10" height="100%" width="100%">
        <Heading size="4xl" letterSpacing="tight">
          Create a New Application
        </Heading>
        <Box marginY="10">
          <Field.Root maxW="36rem" my="5" required>
            <Field.Label>
              Application Name
              <Field.RequiredIndicator />
            </Field.Label>
            <Input
              value={appName}
              onChange={(e) => setAppName(e.target.value)}
              placeholder="Python-app-1"
              width="400px"
            />
          </Field.Root>
          <Select.Root
            value={runtimeSelect}
            onValueChange={(e) => setRuntimeSelect(e.value)}
            collection={runtimeList}
            size="sm"
            width="320px"
          >
            <Select.HiddenSelect />
            <Select.Label>Select framework</Select.Label>
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
          <Button
            disabled={!runtimeSelect.length || isEmptyString(appName)}
            onClick={handleSubmit}
            my="5"
          >
            Create Application
          </Button>
        </Box>
      </Container>
    </Box>
  );
};
