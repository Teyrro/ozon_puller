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
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"

import {
  type ApiError,
  type IUserRead,
  type IUserUpdateMe,
  UserService,
} from "../../client"
import useAuth from "../../hooks/useAuth"
import useCustomToast from "../../hooks/useCustomToast"

const UserInformation = () => {
  const queryClient = useQueryClient()
  const color = useColorModeValue("inherit", "ui.light")
  const showToast = useCustomToast()
  const [editMode, setEditMode] = useState(false)


  const { user: currentUser } = useAuth()
  const {
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting, isDirty },
  } = useForm<IUserRead>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      name: currentUser?.data?.name,
      surname: currentUser?.data?.surname,
    },
  })


  const toggleEditMode = () => {
    setEditMode(!editMode)
  }

  const mutation = useMutation({
    mutationFn: (data: IUserUpdateMe) =>
      UserService.userUpdateUserMe({ requestBody: data }),
    onSuccess: (data) => {
      showToast("Success!", "User updated successfully.", "success")
      queryClient.setQueryData(["currentUser"], data)
      if (data?.data != null) {
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

  const onSubmit: SubmitHandler<IUserUpdateMe> = async (data) => {
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
            <FormLabel color={color} htmlFor="name">
              Name
            </FormLabel>
            {editMode ? (
              <Input
                id="name"
                {...register("name", { maxLength: 30 })}
                type="text"
                size="md"
              />
            ) : (
              <Text
                size="md"
                py={2}
                color={!currentUser?.data?.name ? "ui.dim" : "inherit"}
              >
                {currentUser?.data?.name || "N/A"}
              </Text>
            )}
          </FormControl>
          <FormControl>
            <FormLabel color={color} htmlFor="surname">
              Surname
            </FormLabel>
            {editMode ? (
              <Input
                id="surname"
                {...register("surname", { maxLength: 30 })}
                type="text"
                size="md"
              />
            ) : (
              <Text
                size="md"
                py={2}
                color={!currentUser?.data?.surname ? "ui.dim" : "inherit"}
              >
                {currentUser?.data?.surname || "N/A"}
              </Text>
            )}
          </FormControl>
          {/*TODO: Is it worth to add email form here ?*/}
          {/*<FormControl mt={4} isInvalid={!!errors.email}>*/}
          {/*  <FormLabel color={color} htmlFor="email">*/}
          {/*    Email*/}
          {/*  </FormLabel>*/}
          {/*  {editMode ? (*/}
          {/*    <Input*/}
          {/*      id="email"*/}
          {/*      {...register("email", {*/}
          {/*        required: "Email is required",*/}
          {/*        pattern: emailPattern,*/}
          {/*      })}*/}
          {/*      type="email"*/}
          {/*      size="md"*/}
          {/*    />*/}
          {/*  ) : (*/}
          {/*    <Text size="md" py={2}>*/}
          {/*      {currentUser?.data?.email}*/}
          {/*    </Text>*/}
          {/*  )}*/}
          {/*  {errors.email && (*/}
          {/*    <FormErrorMessage>{errors.email.message}</FormErrorMessage>*/}
          {/*  )}*/}
          {/*</FormControl>*/}
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

export default UserInformation
