import {
    Button,
    Container,
    Flex,
    Heading,
    Skeleton, Stack,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
} from "@chakra-ui/react"
import {useSuspenseInfiniteQuery} from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"

import { Suspense } from "react"
import { ErrorBoundary } from "react-error-boundary"
import {IGetResponsePaginated_IOzonReportRead_, ReportService} from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"

export const Route = createFileRoute("/_layout/reports")({
  component: Reports,
})

function ItemsTableBody() {
 const {
    fetchNextPage,
    fetchPreviousPage,
    data: message,
 } = useSuspenseInfiniteQuery<IGetResponsePaginated_IOzonReportRead_>({
    queryKey: ["items"],
    queryFn: ({pageParam}) => ReportService.reportGetAllReports({page: pageParam}),
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
      {message.pages.map((items) => (
          items.items.map((item) => (
            <Tr key={item.id}>
              <Td>{item.report_type}</Td>
              <Td color={!item.ozon_created_at ? "ui.dim" : "inherit"}>
                {item.ozon_created_at || "N/A"}
              </Td>
              <Td color={!item.created_at ? "ui.dim" : "inherit"}>
                  {item.created_at}
              </Td>
              <Td>
                <ActionsMenu type={"Item"} value={item} />
              </Td>
            </Tr>
          ))
      ))}
        <Tr>
            <Td>
                <Stack direction="row" spacing={4}>
                    <Button
                        // isLoading

                        variant="primary"
                        gap={1}
                        fontSize={{ base: "sm", md: "inherit" }}
                        loadingText="Processing"
                        onClick={() => fetchPreviousPage()}
                    >
                        Prev Page
                    </Button>
                    <Button
                        variant="primary"
                        gap={1}
                        fontSize={{ base: "sm", md: "inherit" }}
                        loadingText="Processing"
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
function ItemsTable() {
  return (
    <TableContainer>
      <Table size={{ base: "sm", md: "md" }}>
        <Thead>
          <Tr>
            <Th>Report Type</Th>
            <Th>Ozon Created At</Th>
            <Th>Created At</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <ErrorBoundary
          fallbackRender={({ error }) => (
            <Tbody>
              <Tr>
                <Td colSpan={4}>Something went wrong: {error.message}</Td>
              </Tr>
            </Tbody>
          )}
        >
          <Suspense
            fallback={
              <Tbody>
                {new Array(5).fill(null).map((_, index) => (
                  <Tr key={index}>
                    {new Array(4).fill(null).map((_, index) => (
                      <Td key={index}>
                        <Flex>
                          <Skeleton height="20px" width="20px" />
                        </Flex>
                      </Td>
                    ))}
                  </Tr>
                ))}
              </Tbody>
            }
          >
            <ItemsTableBody />
          </Suspense>
        </ErrorBoundary>
      </Table>
    </TableContainer>
  )
}

function Reports() {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        Items Management
      </Heading>

      {/*<Navbar type={"Item"} />*/}
      <ItemsTable />
    </Container>
  )
}
