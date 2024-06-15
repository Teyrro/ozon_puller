import {
  Button,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  useDisclosure,
} from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { FiEdit, FiTrash } from "react-icons/fi"
import EditUser from "../Admin/EditUser"

import Delete from "./DeleteAlert"
import {IOzonReportRead, IUserRead} from "../../client";
import {DownloadIcon} from "@chakra-ui/icons";
import Download from "./Download.tsx";

interface ActionsMenuProps {
  type: string
  value: IOzonReportRead | IUserRead
  disabled?: boolean
}

const ActionsMenu = ({ type, value, disabled }: ActionsMenuProps) => {
  const downloadModal = useDisclosure()
  const editUserModal = useDisclosure()
  const deleteModal = useDisclosure()

  return (
    <>
      <Menu>
        <MenuButton
          isDisabled={disabled}
          as={Button}
          rightIcon={<BsThreeDotsVertical />}
          variant="unstyled"
        />
        <MenuList>
          {
            type === "Item" &&
                (<MenuItem
                    onClick={downloadModal.onOpen}
                    icon={<DownloadIcon fontSize="16px"/>}
                >
                  Upload
                </MenuItem>)
          }
          {
            type === "User" &&
                (<MenuItem
                  onClick={editUserModal.onOpen}
                  icon={<FiEdit fontSize="16px" />}
                >
                  Edit {type}
                </MenuItem>)
          }
          <MenuItem
            onClick={deleteModal.onOpen}
            icon={<FiTrash fontSize="16px" />}
            color="ui.danger"
          >
            Delete {type}
          </MenuItem>
        </MenuList>
        {
            type === "Item" &&
            (
                <Download
                  type={type}
                  id={value.id}
                  isOpen={downloadModal.isOpen}
                  onClose={downloadModal.onClose}

                />
            )
        }
        {
          type === "User" ?
              (
                  <EditUser
                      user={value as IUserRead}
                      isOpen={editUserModal.isOpen}
                      onClose={editUserModal.onClose}
                  />
              ) : null
        }
        <Delete
          type={type}
          id={value.id}
          isOpen={deleteModal.isOpen}
          onClose={deleteModal.onClose}
        />
      </Menu>
    </>
  )
}

export default ActionsMenu
