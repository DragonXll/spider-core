import base64
import calendar
import time
import urllib

import requests
import execjs
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
# 获取session
def getSession():
    url = 'http://120.221.95.83:6080/login.jsp'

    params = {
        'ticketId': '',
    }
    data = {
        'keys': 'aG9saWRheXMsd29ya0RheXMsZWlhT2ZDb25zdHJ1Y3Rpb24sZWlhUGxhbm5pbmcsc29pbEFzc2Vzc21lbnQsc29pbEVmZmVjdCx3YXRlclByb3RlY3Rpb24sd2FzdGVQZXJtaXRzLHdhc3RlU3RvcmFnZSxrc1RyYW5zZmVyUGxhbklzTmVlZFRyYW5zcG9ydCxsb2dpblBhc3NNb2JpbGUsb3BlblBob25lVmVyaWZ5LGdlbmVyYWxSZWNvcmRQb2ludE51bSxpc0FsbG93Q2hhbmdlQXNzZXNzbWVudCxrc1BsYW5Jc0hhdmVXaGl0ZVJlcGx5LGNma3NUcmFuc2Zlck91dFdhc3RlSXNFcVBsYW4sY291bnRyeU1hbmlmZXN0SXNEaXNFbnRDYW5jZWwsaXNRdWVyeU1lZGljYWxSZWdpc3QsaHVuYW5TU09VcmwsZ2VuZXJhbENyb3NzUHJvdmluY2VPdmVyWWVhcixpc09wZW5TaGFyZVR5cGUsY291bnRyeVN5c3RlbUNhbGxiYWNrVXJsLGlzQXV0b0NoZWNrVG9rZW4sY29ubmVjdEluZHVzdHJpYWxJbnRlcm5ldCxpc1Jldmlldyx0cmFuc3BvcnRFeGVtcHRpb25BcnJpdmVJc0N6LGh1YVdlaVVybEZvclZpZGVvLGludmVudG9yeURpc05lZWRBdWRpdCxpc1Nob3dNYW5pZmVzdE91dEZpbGVCdXQsc2hvd0VwYUVudExpc3RCYWNrQnV0LGFlc1NlY3VyaXR5S2V5LHN3aXRjaE1lbnVPbixpc0FuaHVpSW50cmFuZXRFbnZpcm9ubWVudCxzaG93U3RvcmFnZVFyY29kZUJ0LGhpa1lzeVRva2VuVXJsLGhpa1lzeUJpbmREZXZpY2VJbmZvVXJsLG9uZU1hcFVybCxIaWtBbkZhbmdWaWRlb1VybCxjYW1lcmFJc1VzZUxpc3QsaWZTaW1wbGlmeUxpY2VuY2Usd29ya0NvbmZpZ1ZpZXdVcmwsaXNEb2NraW5nU2NDbG91ZCx3ZWJTaXRlUm9vdCxmaWxlVXBsb2FkVXJsLHByaW1ldG9uRmlsZSxhcmVhQ29kZSxhcmVhTmFtZSxpb3RWaWRlb1VybCxpb3RNb25pdG9yQ29uZmlndXJhdGlvblVybCxpc09wZW5JbmZvUHVibGljLGlzTWFuYWdlbWVudFBsYW5QdWJsaWNUYWJsZXMsdXJsU2VjcmV0LG1lZGljYWxUcmFuc2VmZXJFbnRyeUNvbmZpZyxpc0RvY2tpbmdDb3VudHJ5RGF0YSxwcm9qZWN0TmFtZSxyZXF1ZXN0U291cmNlUHJvamVjdE5hbWUscmVxdWVzdFNvdXJjZUFwcENvZGUscmVxdWVzdFNvdXJjZUFyZWFOYW1lLHJlcXVlc3RTb3VyY2UscHJvamVjdE5hbWVGb3JNZWRpY2FsLGlzQWxsb3dQdWJsaWNJbmZvLGVudEF0dHJpYnV0ZSxhbnN3ZXJGdW5jdGlvblN3aXRjaCxpc0VuYWJsZVByb2R1Y2VNb250aGx5LGlzRW5hYmxlRGlzcG9zZU1vbnRobHksaXNBYnV0Q291bnRyeUVudERhdGEsaXNTdXBwbHlXcml0ZUVudGVycHJpc2UsZW50ZXJwcmlzZUZpbGVZb25nSG9uZ1VybCxtZWRpY2FsRGF5UmVwb3J0RXBhLG1lZGljYWxEYXlSZXBvcnRFbnQsc2hvd0dwc0J1dHRvbixpZk1vbnRoUmVwb3J0TmVlZEFkdWl0LGlmU2hvd0xhcmdlU2NyZWVuLGlmU2hvd0xhcmdlU2NyZWVuQnV0dG9uLGNpdHlTdXBlcnZpc2UsdXNlTmV3V2FzdGVUeXBlLHVzZU5ld01hbmFnZW1lbnRQbGFuLGlmU2hvd09sZE1vbnRobHlCdXR0b24saW90UHJvamVjdEhiYXNlVXJsLGVudFR5cGVDb25maWcsZ2lzV2ViVXJsLGlzRGlzT3RoZXJQcm92aW5jZVJlY2VpdmVFbnQsZW50VHlwZU90aGVyQ29uZmlnLGlzVXNlUHJvZHVjdGlvbixpc1VzZUxhYm9yYXRvcnksaXNVc2VNZWRpY2F0aW9uLGlzVXNlSW5kdXN0cmlhbFdhc3RlLGlzVXNlU2x1ZGdlUHJvZHVjdGlvbixpc1VzZVNsdWRnZURpc3Bvc2l0aW9uLGlzVXNlVHJhbnNwb3J0YXRpb24saXNVc2VTY2llbnRpZmljVW5pdmVyc2l0eSxpc1VzZUxhbmRmaWxsRGlzcG9zaXRpb24sZW50QXR0clR5cGVDb25maWcsZW50QXR0clR5cGVPdGhlckNvbmZpZyx0cmFuc2Zlck1hbmlmZXN0QXNzb2NpYXRlZE1hbmFnZW1lbnRQbGFuVGltZU91dERheXMsZWlhTGlua1dhc3RlLGFkZE1hdHRlckNoZWNrUmVjb3JkLGFkZEFkbWlzc2lvbkFuYWx5c2lzLHByb2R1Y3RMaW5rV2FzdGUsaXNTdXBwb3J0TXVsdGlwbGVUcmFuc3BvcnQsaXNNYW5pZmVzdFNlbGVjdFBsYW5UcmFuc3BvcnRFbnQsaXNFbmFibGVUcmFuc2Zlck1hbmlmZXN0UGxhbixzeXN0ZW1IZWxwQ29uZmlnLGF1dGhQaG9uZUZvckRhdGEsc2VydmljZVByb2R1Y3Rpb25RUSxzZXJ2aWNlRGlzcG9zaXRpb25RUSxzZXJ2aWNlVGVsLGVwYUFkZERpc3Bvc2FsRW50LGlzT3RoZXJQcm92aW5jZURpc3Bvc2l0aW9uUmVnaXN0ZXJJbmZvQXVkaXQsaXNPdGhlclByb3ZpbmNlVHJhbnNwb3J0YXRpb25SZWdpc3RlckluZm9BdWRpdCxpc090aGVyUHJvdmluY2VQcm9kdWN0aW9uUmVnaXN0ZXJJbmZvQXVkaXQsc2x1ZGdlTWFuaWZlc3RDb2RlUnVsZSxpZkluY2x1ZGVCYXR0ZXJ5LHN5c3RlbVR5cGVDb25maWcsdHJhbnNwb3J0RW50RGF0YURvY2tpbmcsYXVkaXRNYW5hZ2VtZW50UGxhbldpdGhXYXN0ZUVudEluZm8saXNTZWxlY3RNYW5hZ2VQbGFuVHJhbnNwb3J0LGNyZWF0ZU1hbmlmZXN0UmV0dXJuV2FpdEluU3RvcmFnZVRpbWUsaXNTdXBwb3J0U3RyZWV0TWFuYWdlLGlzTmVlZERpc0VudENvbmZpcm1Ob2RlLG1hbmFnZVBsYW5IYXNDcm9zc0FwcHJvdmFsLG1hbmFnZVBsYW5IYXNQcm90b2NvbCxpc1RyYW5zZmVyTWFuaWZlc3RFdmFsdWF0ZSxsb2dpblVybCxpc0VuYWJsZUxpY2VuY2VSYW5nZSxpc1RyYW5zcG9ydEV4ZW1wdGlvbixpc0FsbG93TWFuaWZlc3RVbnBhY2tUcmFuc2ZlcixwbGFuT3V0Q2hlY2ssbWFuaWZlc3RPdXRDaGVjayxpc1JlY29yZExvZ2luT3JMb2dvdXQsdHJhbnNwb3J0RW50U2pSdWxlLGFyZWFBcHBseUNvbmZpZyxpc0JpZ0JveFRvTGl0dGxlQm94LG51bWJlck9mQmVkLGlzUmVxdWlyZUxpdHRsZUJveCxpc1VzZVRyYW5zUG9ydCxpc0F1dG9PaWwsaXNTaGlwRm91bFdhdGVyLGlzVHJhbnNwb3J0SW5mb1dyaXRlQnlUcmFuc0VudCxpc01lZGljYWxJbmZvVG9HdUNodUNlbnRyZSxpc09wZW5NaWNyb0VudCxpc0Nsb3NlU29saWRXYXN0ZUxvZ2luLG1pY3JvRW50U2NvcGUsYXVkaXRTeXN0ZW1VcmwsaWZOZWVkQWNjZXB0LHRyYW5zZmVyUGxhblVwbG9hZEZpbGUsaXNVc2VFbnRDaGVja0l0ZW0saXNVc2VNZWRpY2FsQnVzaW5lc3NMaWNlbnNlTm8sbGljZW5zZUJhc2VJbmZvTmVlZEV4dGVuZEZpbGUsaXNTZWNvbmRDYXJyaWVyLGxpY2Vuc2VBdWRpdE5lZWRBcHBseURvYyxsaWNlbmNlQXBwcm92YWxRdWFudGl0eVJ1bGUsaXNMaWNlbnNlQXBwcm92YWxOYW1lLGlzQXV0b0dlbmVyYXRlQXBwcm92YWxRdWFudGl0eSxsaWNlbmNlQXBwcm92YWxRdWFudGl0eUNhbGN1bGF0ZUJ5TW9udGgsaXNTaG93RGVmYXVsdEluZm9JbkF1ZGl0TGljZW5jZSxpc0xpY2Vuc2VBdXRoVHlwZSxpZkVuYWJsZUNob29zZVVuaXRGb3JMaWNlbmNlLG1hbmFnZW1lbnRQbGFuV2FzdGVRdWFudGl0eVN1bUJhbGFuY2UsZ3VpZGVJY29uLHJlcXVlc3RTb3VyY2VTaG93R3VpZGVJY29uLGlzRWlhUHJvamVjdEF1ZGl0LGZpcnN0TG9naW5MaW1pdCxmaXJzdExvZ2luTGltaXRFbnQsaXNVc2VNZWRpY2FsUmVnaXN0cmF0aW9uTm8sbWVudUJlbG9uZ0tleSxyZWxhdGVkQnVzaW5lc3NVc2VOZXdMaWNlbmNlLHN0b2NrTW9kaWZ5RGF0ZUxpbWl0LGhhdmVQb2xsdXRlU291cmNlQ29kZSxwb2xsdXRlU291cmNlVXJsLG1hbmFnZW1lbnRQbGFuTGFzdFllYXJJbWJhbGFuY2VBbGxvd1RvU3VibWl0LGluZGV4UGFnZU1zZyxpc1Nob3dBbGxSZWFkLHBvbGx1dGlvblNvdXJjZXNUb2tlblhKLG9wZW5TdG9ja01vZGlmeURhdGVMaW1pdCxnZW5lcmFsV2FzdGVJc09wZW5TdG9jayxob21lUGFnZVNob3dXYXJuaW5nLGFwcENvZGUsUVJDb2RlVXJsLGlzU2VydmljZVRlc3QsYmF0dGVyeVBpbG90RW50TWFuYWdlQ29sbGVjdGluZ1BvaW50QnlFbnRBdHRyLGJhdHRlcnlXYXN0ZUlkcyx1c2VyU21zRm9yQWRkVXNlcixiYXRCdXNpbmVzc1R5cGUsd2RTdG9yYWdlRGF5cyx6eVN0b3JhZ2VEYXlzLGlmTmVlZENvbmZpcm1Gb3JBY2NvdW50LGlmQWxsb3dTZWNvbmRGb3JBY2NvdW50LGJhY2tVcmxGb3JHcyxiYWNrVXJsRm9yR3NIb21lLGxvZ2luQ2FsbEJhY2sseW9uZ0hvbmdTeXNGbGFnLGlzRGlzY2hhcmdlTGljZW5jZSxpc0NoZW1pY2FsSW5kdXN0cnlQYXJrLGlzU2F2ZUVudGVycHJpc2VTdXBlcnZpc2VMZXZlbCxiYXR0ZXJ5Q29sbGVjdGluZ1dheSxpc1VzZVRhaWxpbmcsaXNTdXBwb3J0SGFuZEZpbGwsaXNMaWNlbmNlRWRpdEFkZEVpYVByb2plY3QsaXNVc2VHYXJiYWdlLGFubnVhbERlY2xhcmF0aW9uTGljZW5jZSxpc09wZW5OZXdPbGRXYXN0ZURvY2sscHJvZHVjZVllYXJSZXBvcnRFbnRDb2RlTGltaXQsaXNQcm92aW5jZU1hbmlmZXN0UGxhblRyYW5zcG9ydEVudCxhcHBTdGF0aXN0aWNzQ29uZmlnLGJhdHRlcnlXYXN0ZUNvZGUsaXNTaG93TmF0aW9uYWxEb2NraW5nV2l0aERlY2xhcmF0aW9uLGRlY2xhcmVZZWFyV2l0aE5hdGlvbmFsRG9ja2luZyxpc1Nob3dOYXRpb25hbERvY2tpbmdXaXRoUGxhbixpc1Nob3dOYXRpb25hbERvY2tpbmdXaXRoTWFuaWZlc3QsZmpfRXhpc3RMb2dpblVybCxwYXNzd29yZFN0cmVuZ3RoQ2hlY2sscGFzc3dvcmRIaWdoU3RyZW5ndGgsdXNlck5hbWVMb2dpbixob21lVXJsLGlzT3BlblRyYW5zcG9ydEV4ZW1wdGlvbixkaWZmSW5kdXN0cnlTb3VyY2UsZ2VuZXJhbFRyYW5zZmVyUGxhblRpbWVMaW1pdCxnZW5lcmFsVHJhbnNmZXJQbGFuQXVkaXRVcmwsaXNTaG93RGFuZ2Vyb3VzQ2hlbWljYWwsY2l0eUF1ZGl0TWFuYWdlbWVudFBsYW5JZldhc3RlQ2hhbmdlLGlzTWFuYWdlUGxhblRoaXJkQXVkaXQsbWVkaWNhdGlvbkVudEJ1c2luZXNzSW5jbHVkZU5vcm1hbFdhc3RlLHhpYU1lblJlc291cmNlVXJsLGhpc3RvcnlBdXRvRGVjbGFyYXRpb25TaG93LGhpc3RvcnlBdXRvRGlzcG9zZURlY2xhcmF0aW9uU2hvdyxtYW5hZ2VtZW50UGxhbk5vQ2hlY2tMYXN0WWVhclZhbHVlLHRyYW5zcG9ydEV4ZW1wdGlvblNtc0NyZWF0ZSx0cmFuc3BvcnRFeGVtcHRpb25TbXNPdXQsbWFuaWZlc3RDcmVhdGVSZXBsZW5pc2gsbWFuaWZlc3RTaWduUmVwbGVuaXNoLG1hbmlmZXN0QXJyaXZlUmVwbGVuaXNoLGxpbWl0QXBwbHlRdWFudGl0eUFuZFRyYW5zZmVyUXVhbnRpdHksaXNQaXBlVHJhbnNmZXJNYW5pZmVzdFBsYW4sZGljdGlvbmFyeVN0b3JhZ2UsaXNNaW5pVHJhbnNmZXJNYW5pZmVzdFBsYW4saXNOZWVkQ2hlY2tZZWFyUmVwb3J0LHNtc1ZlcmlmaWNhdGlvbkNvZGVFZmZlY3RpdmVUaW1lLGlzRGVjbGFyZUZpbGxPdGhlck1lZGljYWxQcm9kdWN0aW9uLHZlcmlmaWNhdGlvblVzZVdheSxpc0RvY2tpbmdHb3ZOZXRGb3JBbkgscmVjb3JkRmlsZSxpc1VzZUVwYVJlQ2hlY2tGb3JKaW5nWWluZ05pYW5CYW8saXNPcGVuUmVnaXN0ZXIsbmVlZFdyaXRlVHJhbnNQb3J0LGluZGV4VXJsLGlzU2hvd0VudGVycHJpc2VUYWcsaXNBZGRTb2NpYWxTb3VyY2UsaHVuYW5SZWdpc3RlclBhZ2UsaXNOZWVkQ2hlY2tlZEFnYWluLGlzU2hvd0dlbmVyYWxXYXN0ZUNvZGUsaXNEb3duTG9hZEZpbGUsaXNMb2dpbkNoZWNrUGFzc3dvcmQscGFzc3dvcmRWYWxpZGl0eVBlcmlvZCxwYXNzd29yZE1pbkxlbmd0aCxwYXNzd29yZE1heExlbmd0aCxwYXNzd29yZENvbWJpbmF0aW9uVHlwZSxwYXNzd29yZE5vdEFsbG93ZWRDb25zZWN1dGl2ZU51bWJlcixrc0dlbmVyYWxJbixrc0dlbmVyYWxPdXQsc3lzQ29weVJpZ2h0VGV4dCxpc09wZW5TZWxmQ2hlY2ssY2hhbmdlVG9OQ1VybCxjaGFuZ2VUb0pYVXJsLGlzRm9yY2VBY2NvdW50QmluZFBob25lLGlzQWxsb3dIQkRSZXR1cm5QYXNzUGxhbixmalVzZXJBdXRoZW50aWNhdGlvbixmal9jaGVja0xvZ2luQmFja3VybCxmalJlY29yZEluZm8sZmpfY2FsbGVyQ29kZSxmal9yZWdpc3RlclVybCxpc05lZWRXYXN0ZUZhY2lsaXR5LGlzTmVlZEhCSlJlY29yZFBhc3NNYW5hZ2VtZW50UGxhbixzZWNvbmRhcnlNYW5hZ2VtZW50T2ZCYXR0ZXJpZXMsdXNlQmF0dGVyeVRyYW5zU3RvcmFnZSxpc1VzZUVudE1hbmNhdGVnb3J5LGlzRXBhVXBkYXRlTWFuY2F0ZWdvcnksbW9iaWxlVHJhbnNPdXRSZWNvcmRHUFMsbW9iaWxlTXVzdFRyYW5zT3V0UmVjb3JkR1BTLG1vYmlsZVRyYW5zT3V0UmVjb3JkR1BTVHJhbnNUeXBlLGFjY2VwdExpbWl0RXh0cmFPcHRpb25zLGluY29taW5nQW5hbHlzaXMsZW50ZXJwcmlzZU1vZGVsWEpUZW1wbGF0ZSxpc1BvbGx1dGlvbkNvbnRyb2wsaXNFeGNlcHRpb25Ob3RpY2VSZXBseSxpc0hvcml6b250YWxTY3JlZW4saXNTaG93Q29tcHJlc3NEb3dubG9hZCxvcGVuQ2hlY2tTaXR1YXRpb24sZmpRaW5RaW5nVXJsLGlzT3Blbk1hbmFnZW1lbnRQbGFuR3JhZGVSZWNvcmQsc29jaWFsU291cmNlSW5mb3JtYXRpb24sZW50ZXJwcmlzZUFwcGx5RG93bmxvYWRUZW1wbGF0ZSxpc0FjY29yZGluZ1RvRGlzcG9zYWxVc2luZ1NlbGYsaXNMaW1pdEVudEVudGVySW52ZW50b3J5LGJhdHRlcnlUcmFuc2ZlclBsYW5Td2l0Y2gsbWFuYWdlbWVudFBsYW5EYXlzUmVjb3JkLHRyYW5zZmVyTWFuaWZlc3RSZXR1cm5Pbmx5Q2l0eVJlY29yZCxiaWdTY3JlZW5Sb2xlQ29kZSxiaWdTY3JlZW5VcmwsaXNVc2VTY2FDb2xsZWN0aW5nV2F0ZUh1b01pYW4saXNVc2VEaXNwb3NpdGlvbkh1b01pYW4sb3BlblJvbGVNb2R1bGUsaXNHZXRNYW5pZmVzdE5vRnJvbUNvdW50cnlTeXN0ZW0saXNOZWVkVHJhbnNwb3J0RW50QXJyaXZlLGNvdW50cnlTeXN0ZW1Ub2tlblVybCxjb3VudHJ5U3lzdGVtUHV0QmlsbERhdGFVcmwsY291bnRyeVN5c3RlbVdlYlBhZ2VVcmwsY291bnRyeVN5c3RlbUFwcFBhZ2VVcmwsaXNOZWVkVmVyaWZ5Q291bnRyeVRyYW4saXNBbGxvd1JlY2VpdmVFbnRJblN0b2NrQ2hhbmdlV2FzdGVOYW1lLGlzVXNlS3NUcmFuc2ZlclBsYW5XaGl0ZUxpc3QsbGljZW5jZVdhdGVyTWFyayxpc0tzVHJhbnNJbk1hdGVyaWFsTWF0Y2hCeUF1ZGl0U3lzdGVtLGlzT3BlblBvaW50UmVjb3JkLGlzT3BlbkRlY2xhcmF0aW9uUmVtaW5kLHJlY29yZEluZm8sbWFuYWdlbWVudFN5c3RlbVVybCx0b1dlaUZhbmdVcmwsdHJhbnNwb3J0V2ZFcnJvclVybCx0cmFuc3BvcnRXZlVybCxIQldKR19IRUFERVIsaXNPcGVuQXV0b0RlY2xhcmF0aW9uLGlzT3BlblRvV2VpRmFuZ1VybCx3ZWJJbmZvcm1hdGlvbklmcmFtZVVybCxpZlllYXJSZXBvcnROZWVkQWR1aXQsYWhMb2dPdXRVcmwsQVBQX0NPREVfQUgsYWhMb2dpbkdvdk5ldFVybCxpc09wZW5FeHBvcnQsaXNVc2VXZlVJU3RhbmRhcmQsaXNFeGNlcHRpb25OZWVkUHVzaCxpc0Nsb3NlU3RvcmFnZUFkanVzdEJ1dHRvbixpc0NoZW1pY2Fsc05lZWRBdWRpdCx1c2VNZWRpY2FsV2FzdGVTdG9yYWdlLGlzQ2FyckVudCxzeXN0ZW1Db250YWN0TWV0aG9kLGlzRGlzYWJsZVVuaXRQZWFjZSxjb2xsZWN0TWVkaWNhbEF1dG9GaWxsRm9ybSxjb2xsZWN0TWVkaWNhbEl0ZW1SZXF1aXJlZCxpc0V4Y2VwdGlvbkdyb3VwQnlMZXZlbCxpc0FsbG93QmF0dGVyeUNoYW5nZU5hbWVBbmRBZGp1c3RCdXNpbmVzcyxpc09wZW5Tb2lsVHJhbnNmZXIsbmV3TWFuYWdlbWVudFBsYW5VcmwsaXNVc2VRdWFydGVybHlSZXBvcnQsaXNRdWFydGVybHlSZXBvcnRUb1Bhc3Msbm90QWxsb3dUcmFuc2Zlck1vbnRocyxpc09wZW5Lc0luQXVkaXRRdWFudGl0eVJlcGxhY2UsaXNFeHBvcnRJbnZlbnRvcnlCaWxsLGlzRXhwb3J0VHJhbnNmZXJJbkFwcGx5LGlzT3BlbkV2YWx1YXRlQnRuLG9wZW5Jbml0SW52ZW50b3J5VmVyaWZpY2F0aW9uLG5ld01hbmFnZVBsYW5Qcm9qZWN0TmFtZSxoYkFwcFVybA=='
    }
    response = requests.post(url, json=data, params=params)
    cookie = requests.utils.dict_from_cookiejar(response.cookies)
    session = cookie["SESSION"]
    return session


# 时间戳
def getTimeStamp():
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    return time_stamp


# 验证码图片下载位置
path = dir_path+'/image/captcha.png'
#path = '/xizheng/py/wastes/wasteless_city/image/captcha.png'
# 百度识别账号与密码
API_KEY = "groaSgDrECGhtXRavZ6yQ04i"
SECRET_KEY = "FIKPOIGxEYGD7lhEInqMGtdqc1CqgR4G"


# 请求下载验证码图片
def downLoadCaptcha(session):
    # session = getSession()
    cookies = {
        'SESSION': session,
    }
    response = requests.post(
        url='http://120.221.95.83:6080/enterprise/user/getVerificationCodeView?etc=' + str(getTimeStamp()),
        cookies=cookies)

    with open(file=r''+dir_path+'/image/captcha.png', mode='wb') as g:
        g.write(response.content)
    # with open(file=r'/xizheng/py/wastes/wasteless_city/image/captcha.png', mode='wb') as g:
    #     g.write(response.content)


# 编码
def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


# 获取百度识别的access_token
def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


# 加密方法
def get_js():
    f = open(dir_path+"/js/RSA.js", 'r', encoding='UTF-8')
    #f = open("/xizheng/py/wastes/wasteless_city/js/RSA.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


# 识别下载的验证码图片
def identifyCaptcha(session):
    # 下载
    downLoadCaptcha(session)
    # 识别
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token()
    newNUm1 = str(get_file_content_as_base64(path)).replace("=", "%3D")
    newNUm2 = newNUm1.replace("+", "%2B")
    newNUm3 = newNUm2.replace("/", "%2F")
    newNUm = 'image=' + newNUm3
    payload = newNUm
    response = requests.request("POST", url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }, data=payload)
    print(response.json())
    list = response.json()["words_result"]
    for i in range(1):
        code = list[0]["words"]
    return code


class Singleton:
    _instance = None

    def login(self, session):
        # 获取加密方式
        js = get_js()
        # 获取验证码
        captchaCode = str(identifyCaptcha(session))
        # 处理登录信息
        ctx = execjs.compile(js)
        account = ctx.call('FWRSAHelper.encrypt', '18000370212')
        password = ctx.call('FWRSAHelper.encrypt', '123qweASD#')
        value = password + ',' + captchaCode
        passwordCaptcha = ctx.call('FWRSAHelper.encrypt', value)
        response = requests.post(
            'http://120.221.95.83:6080/enterprise/user/enhanceLogin',
            params={
                'etc': str(getTimeStamp())
            },
            cookies={
                'SESSION': session,
                'Hm_lvt_0aabb31005445bec1e2759bd1a8a8485': '1676528819,1676528889,1676534126,1676595887',
                'Hm_lpvt_0aabb31005445bec1e2759bd1a8a8485': '1676595887',
            },
            headers={
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://120.221.95.83:6080',
                'Referer': 'http://120.221.95.83:6080/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
            },
            data={"phoneNum": account,
                  "password": passwordCaptcha,
                  "verificationCode": captchaCode,
                  'smsCode': '',
                  "cantonCode": "00",
                  "cantonName": "未知",
                  "clientIp": "127.0.0.1",
                  'commonWay': '',
                  },
            verify=False,
        )
        # 获取登录后返回的=信息
        list = response.json()["extend"]
        print(list['ticketId'])
        self._instance = list['ticketId']
        return self._instance

    def __init__(self):
        print("An instance of Singleton was created.")
