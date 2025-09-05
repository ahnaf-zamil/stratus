/**
 * Page for creating a new application.
 * Fetches available runtimes, manages form state, and handles submission.
 */

import { appsApi } from "@/api/apps";
import type { RuntimeConfig } from "@/api/interfaces";
import { CreateAppForm } from "@/components/forms/CreateAppForm";
import { createListCollection } from "@chakra-ui/react";
import { Toaster, toaster } from "@/components/ui/toaster";
import type React from "react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { isAxiosError } from "axios";

export const CreateApplicationPage: React.FC = () => {
  // Prevents double-fetching in React 18 Strict Mode
  const hasFetched = useRef(false);

  const [appName, setAppName] = useState<string>("");
  const [runtimeSelect, setRuntimeSelect] = useState<string[]>([]);
  const [gitRepo, setGitRepo] = useState<string>("");

  const [runtimes, setRuntimes] = useState<RuntimeConfig[]>([]);

  // Memoized transformation of runtimes into Chakra-compatible list format
  const runtimeList = useMemo(() => createListCollection({
    items: runtimes.map((runtime) => ({
      label: `${runtime.language} ${runtime.version}`,
      icon: runtime.language,
      value: runtime.id,
    })),
  }), [runtimes]);

  useEffect(() => {
    if (!hasFetched.current) {
      appsApi.getAppRuntimes().then(([data, error]) => {
        if (error) {
          // Show error toast if fetch fails
          toaster.create({
            title: "Failed to fetch application runtimes.",
            description: "Please reload the page.",
            type: "error",
            duration: 5000,
            closable: true,
          });
        } else {
          setRuntimes(data?.data ?? []);
        }
      });
      hasFetched.current = true;
    }
  }, []);

  // Handles form submission and validation
  const handleSubmit = useCallback(async () => {
    if (!appName.trim() || !runtimeSelect.length || !gitRepo.trim()) {
      toaster.create({
        title: "Missing required fields.",
        description: "Please fill out all fields before submitting.",
        type: "warning",
        duration: 4000,
        closable: true,
      });
      return;
    }

    const [resp, err] = await appsApi.createApplication(
      appName,
      runtimeSelect[0],
      gitRepo
    );
    if (err) {
      toaster.create({
        title: `Failed to create application.`,
        description: `Error code ${isAxiosError(err) ? err.response?.status : "unknown"}`,
        type: "error",
        duration: 5000,
        closable: true,
      });
    } else {
      console.log(resp);
      // TODO: Redirect on success
    }
  }, [appName, runtimeSelect, gitRepo]);

  return (
    <>
      {/* Mounts global toaster UI */}
      <Toaster />

      {/* Renders the application creation form */}
      <CreateAppForm
        appName={appName}
        setAppName={setAppName}
        runtimeSelect={runtimeSelect}
        setRuntimeSelect={setRuntimeSelect}
        gitRepo={gitRepo}
        setGitRepo={setGitRepo}
        runtimeList={runtimeList}
        onSubmit={handleSubmit}
      />
    </>
  );
};
