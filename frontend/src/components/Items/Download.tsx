import {
  AlertDialog,

  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogOverlay,
  Button,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import React from "react"
import { useForm } from "react-hook-form"

import {OpenAPI} from "../../client"
import useCustomToast from "../../hooks/useCustomToast.ts"
import axios from "axios";
import {getHeaders, getUrl} from "../../client/core/request.ts";
import type {ApiRequestOptions} from "../../client/core/ApiRequestOptions.ts";
import {saveAs} from "file-saver";




interface DeleteProps {
  type: string
  id: string
  isOpen: boolean
  onClose: () => void
}

const reportDownloadFile = async (reportId: string) => {
  const config = OpenAPI
  const options: ApiRequestOptions =
      {
		    method: 'POST',
			url: '/api/v1/report/download/{report_id}',
			path: {
				report_id: reportId
			},
			errors: {
				422: `Validation Error`,
			},
      }
      const url = getUrl(config, options)
      const headers = await getHeaders(config, options);
  axios({
    method: "POST",
    url: url,
    responseType: "blob",
    params: {
      reportId
    },
    headers: headers
  }).then((res) => {
      const content: string = res.headers["content-disposition"]
      const filename = content.substring(content.indexOf("=") + 1)
      saveAs(res.data, filename, {autoBom: true})
  })
}

const Download = ({ type, id, isOpen, onClose }: DeleteProps) => {
  const queryClient = useQueryClient()
  const showToast = useCustomToast()
  const cancelRef = React.useRef<HTMLButtonElement | null>(null)
  const {
    handleSubmit,
    formState: { isSubmitting },
  } = useForm()

    const uploadFile = (id: string) => (
        reportDownloadFile(id)
    )


  const mutation = useMutation({
    mutationFn: uploadFile,
    onSuccess: () => {

      showToast(
        "Success",
        `The report was pulled successfully.`,
        "success",
      )
      onClose()
    },
    onError: () => {
      showToast(
        "An error occurred.",
        `An error occurred while downloading the ${type.toLowerCase()}.`,
        "error",
      )
    },
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: [type === "Item" ? "items" : "users"],
      })
    },
  })

  const onSubmit = async () => {
    mutation.mutate(id)
  }

  return (

      <AlertDialog
        isOpen={isOpen}
        onClose={onClose}
        leastDestructiveRef={cancelRef}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <AlertDialogOverlay>
          <AlertDialogContent as="form" onSubmit={handleSubmit(onSubmit)}>
            <AlertDialogHeader>Upload {type}</AlertDialogHeader>

            <AlertDialogFooter gap={3}>
              <Button type="submit" isLoading={isSubmitting}>
                Upload
              </Button>
              <Button
                ref={cancelRef}
                onClick={onClose}
                isDisabled={isSubmitting}
              >
                Cancel
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
  )
}

export default Download
