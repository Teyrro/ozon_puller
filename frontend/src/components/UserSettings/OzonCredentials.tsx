import {
  Box,
  Button,
  Container,
  Flex,
  FormControl,
  FormLabel,
  Heading,
  Input,
  Text,
  useColorModeValue,
} from "@chakra-ui/react"
import {useMutation, useQueryClient} from "@tanstack/react-query"
import {useState} from "react"
import { type SubmitHandler, useForm } from "react-hook-form"

import {
  type ApiError, IOzonDataCreate, IOzonDataRead,

  OzonDataService, PartialIOzonDataUpdate,

} from "../../client"

import useCustomToast from "../../hooks/useCustomToast"
import useAuth from "../../hooks/useAuth.ts";

const OzonCredentials = () => {
  const queryClient = useQueryClient()
  const color = useColorModeValue("inherit", "ui.light")
  const showToast = useCustomToast()
  const [editMode, setEditMode] = useState(false)

  // const { user: currentUser } = useAuth()
  const {ozonData: message} = useAuth()
  const ozon_data = message?.data
  const {
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting, isDirty },
  } = useForm<IOzonDataRead>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      client_id: ozon_data?.client_id,
      api_key: ozon_data?.api_key,
    },
  })

  const mutationFn = (data: PartialIOzonDataUpdate | IOzonDataCreate) =>
    OzonDataService.ozonDataUpdateOzonDataMe({ requestBody: data })

  const toggleEditMode = () => {
    setEditMode(!editMode)
  }



  const mutation = useMutation({
    mutationFn: mutationFn,
    onSuccess: (data) => {
      showToast("Success!", "User updated successfully.", "success")
      queryClient.setQueryData(["ozon_data"], data)
      if (data?.data !== null && data?.data !== undefined) {
        reset(data.data)
      }
    },
    onError: (err: ApiError) => {
      const errDetail = (err.body as any)?.detail
      showToast("Something went wrong.", `${errDetail}`, "error")
    },
    onSettled: () => {
      // TODO: can i do just one call now?
      queryClient.invalidateQueries({ queryKey: ["users"] })
      queryClient.invalidateQueries({ queryKey: ["currentUser"] })
    },
  })

  const onSubmit: SubmitHandler<PartialIOzonDataUpdate | IOzonDataCreate> = async (data) => {
    mutation.mutate(data)
  }

  const onCancel = () => {
    reset()
    toggleEditMode()
  }

  return (
    <>
      <Container maxW="full">
        <Heading size="sm" py={4}>
          User Information
        </Heading>
        <Box
          w={{ sm: "full", md: "50%" }}
          as="form"
          onSubmit={handleSubmit(onSubmit)}
        >
          <FormControl>
            <FormLabel color={color} htmlFor="client_id">
              Client ID
            </FormLabel>
            {editMode ? (
              <Input
                id="client_id"
                {...register("client_id", { maxLength: 30 })}
                type="text"
                size="md"
              />
            ) : (
              <Text
                size="md"
                py={2}
                color={!ozon_data?.client_id ? "ui.dim" : "inherit"}
              >
                {ozon_data?.client_id || "N/A"}
              </Text>
            )}
          </FormControl>
          <FormControl>
            <FormLabel color={color} htmlFor="api_key">
              API Key
            </FormLabel>
            {editMode ? (
              <Input
                id="api_key"
                {...register("api_key", { maxLength: 30 })}
                type="text"
                size="md"
              />
            ) : (
              <Text
                size="md"
                py={2}
                color={!ozon_data?.api_key ? "ui.dim" : "inherit"}
              >
                {ozon_data?.api_key || "N/A"}
              </Text>
            )}
          </FormControl>
          <Flex mt={4} gap={3}>
            <Button
              variant="primary"
              onClick={toggleEditMode}
              type={editMode ? "button" : "submit"}
              isLoading={editMode ? isSubmitting : false}
              isDisabled={editMode ? !isDirty : false}
            >
              {editMode ? "Save" : "Edit"}
            </Button>
            {editMode && (
              <Button onClick={onCancel} isDisabled={isSubmitting}>
                Cancel
              </Button>
            )}
          </Flex>
        </Box>
      </Container>
    </>
  )
}

export default OzonCredentials
