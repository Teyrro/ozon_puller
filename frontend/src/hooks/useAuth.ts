import {useMutation, useQuery, useQueryClient} from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { useState } from "react"

import { AxiosError } from "axios"
import {
  type Body_login_access_token as AccessToken,
  type ApiError,
  LoginService,
  UserService, IGetResponseBase_IUserReadWithRole_, OzonDataService
} from "../client"

const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null
}

const useAuth = () => {
  const queryClient = useQueryClient()
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const { data: user, isLoading } = useQuery<IGetResponseBase_IUserReadWithRole_, Error>({
    queryKey: ["currentUser"],
    queryFn: UserService.userReadUserMe,
    enabled: isLoggedIn(),
  })


  const {data: ozonData } = useQuery({
    queryKey: ["ozon_data"],
    queryFn: OzonDataService.ozonDataReadOzonDataMe,
    enabled: user?.data != null,
  })

  const login = async (data: AccessToken) => {
    const response = await LoginService.loginAccessToken({
      formData: data,
    })
    localStorage.setItem("access_token", response.access_token)
  }

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      navigate({ to: "/" })
    },
    onError: (err: ApiError) => {
      let errDetail = (err.body as any)?.detail

      if (err instanceof AxiosError) {
        errDetail = err.message
      }

      if (Array.isArray(errDetail)) {
        errDetail = "Something went wrong"
      }

      setError(errDetail)
    },
  })

  const logout = () => {
    localStorage.removeItem("access_token")
    queryClient.clear()
    navigate({ to: "/login" })

  }

  return {
    loginMutation,
    logout,
    user,
    isLoading,
    error,
    resetError: () => setError(null),
    ozonData,
  }
}

export { isLoggedIn }
export default useAuth
