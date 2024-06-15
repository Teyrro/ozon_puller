import {
  Badge,
  Box, Button,
  Container,
  Flex,
  Heading,
  SkeletonText, Stack,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react"
import { useQueryClient, useSuspenseInfiniteQuery} from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import {Suspense} from "react"
import {
  IGetResponseBase_IUserReadWithRole_,
  IGetResponsePaginated_IUserReadWithRole_,
  UserService
} from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"



export const Route = createFileRoute(
    "/_layout/admin"
)({
  component: Admin,
})

const   MembersTableBody = () => {
  const queryClient = useQueryClient()
  const currentUser = queryClient.getQueryData<IGetResponseBase_IUserReadWithRole_>(
      ["currentUser"]
  )?.data


  const {
    fetchNextPage,
    fetchPreviousPage,
    data: message,

  } = useSuspenseInfiniteQuery<IGetResponsePaginated_IUserReadWithRole_>({
    queryKey: ["users"],
    queryFn: ({pageParam}) => UserService.userReadUsers({page: pageParam, size:50}),
    initialPageParam: 1,
    getNextPageParam: (lastPage) =>
    {
      if (lastPage.page && lastPage.pages && lastPage.page < lastPage.pages)
        return lastPage.page + 1
      else {
        return
      }
    },
    getPreviousPageParam: (firstPage) =>
    {
        if (firstPage.page && firstPage.pages && firstPage.page < 1)
          return firstPage.page - 1
        else {
          return
        }
    }
  })

  return (
        <Tbody>
          {
            message.pages.map((pages) => (
                pages.items.map( (user) => (
                    <Tr key={user.id}>
                      <Td color={!user.name ? "ui.dim" : "inherit"}>
                        {user.name || "N/A"}
                        {currentUser?.id === user.id && (
                          <Badge ml="1" colorScheme="teal">
                            You
                          </Badge>
                        )}
                      </Td>
                      <Td color={!user.surname ? "ui.dim" : "inherit"}>
                        {user.surname || "N/A"}
                      </Td>
                      <Td>{user.email}</Td>
                      <Td>{user.role.name === "admin" ? "Superuser" : "User"}</Td>
                      <Td>
                        <Flex gap={2}>
                          <Box
                            w="2"
                            h="2"
                            borderRadius="50%"
                            bg={user.is_active ? "ui.success" : "ui.danger"}
                            alignSelf="center"
                          />
                          {user.is_active ? "Active" : "Inactive"}
                        </Flex>
                      </Td>
                      <Td>
                        <ActionsMenu
                          type="User"
                          value={user}
                          disabled={currentUser?.id === user.id}
                        />
                      </Td>
                    </Tr>
                ))
            ))
          }<Tr>
            <Td>
              <Stack direction="row" spacing={4}>
                <Button
                    // isLoading

                    variant="primary"
                    gap={1}
                    fontSize={{ base: "sm", md: "inherit" }}
                    onClick={() => fetchPreviousPage()}
                >
                  Prev Page
                </Button>
                <Button
                    variant="primary"
                    gap={1}
                    fontSize={{ base: "sm", md: "inherit" }}
                    onClick={() => fetchNextPage()}
                >
                  Next Page
                </Button>
              </Stack>
            </Td>
          </Tr>
        </Tbody>



  )
}

const MembersBodySkeleton = () => {
  return (
    <Tbody>
      <Tr>
        {new Array(6).fill(null).map((_, index) => (
          <Td key={index}>
            <SkeletonText noOfLines={1} paddingBlock="16px" />
          </Td>
        ))}
      </Tr>
    </Tbody>
  )
}

function Admin() {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        User Management
      </Heading>
      <Navbar type={"User"} />
      <TableContainer>
        <Table fontSize="md" size={{ base: "sm", md: "md" }}>
          <Thead>
            <Tr>
              <Th width="20%">Name</Th>
              <Th width="20%">Surname</Th>
              <Th width="50%">Email</Th>
              <Th width="10%">Role</Th>
              <Th width="10%">Status</Th>
              <Th width="10%">Actions</Th>
            </Tr>
          </Thead>
          <Suspense
              fallback={<MembersBodySkeleton />}
          >
            <MembersTableBody />
          </Suspense>
        </Table>
      </TableContainer>
    </Container>
  )
}
