# LIBRERÍAS
library(shiny)
library(shinydashboard)
library(httr)
library(jsonlite)
library(ggplot2)
library(dplyr)

# FUNCIÓN PARA OBTENER DATOS DE LA API
get_ipc_data <- function() {
  url <- "https://apis.datos.gob.ar/series/api/series/?ids=103.1_I2N_2016_M_19:percent_change&format=json&start_date=2017-01-01"
  res <- httr::GET(url)

  if (httr::status_code(res) != 200) {
    warning("Error al acceder a la API")
    return(data.frame(fecha = as.Date(character()), valor = numeric()))
  }

  json_data <- fromJSON(content(res, as = "text", encoding = "UTF-8"))
  serie <- json_data$series[[1]]

  # Validar que existan valores
  if (length(serie$data) == 0 || is.null(serie$index)) {
    warning("La API devolvió una serie vacía o mal estructurada")
    return(data.frame(fecha = as.Date(character()), valor = numeric()))
  }

  # Intentar convertir a fecha y número
  df <- data.frame(
    fecha = as.Date(serie$index),
    valor = suppressWarnings(as.numeric(serie$data))
  )

  # Eliminar NA o filas inválidas
  df <- df %>% filter(!is.na(fecha) & !is.na(valor))

  return(df)
}

# INTERFAZ DEL USUARIO (UI)
ui <- dashboardPage(
  dashboardHeader(title = "Dashboard IPC Argentina"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Evolución mensual", tabName = "linea", icon = icon("chart-line")),
      menuItem("Comparación anual", tabName = "barras", icon = icon("chart-bar")),
      menuItem("Participación estimada", tabName = "torta", icon = icon("chart-pie"))
    )
  ),
  dashboardBody(
    tabItems(
      # Panel: Gráfico de Línea
      tabItem(tabName = "linea",
              fluidRow(
                box(
                  title = "Evolución del Índice de Precios al Consumidor",
                  status = "primary", solidHeader = TRUE, width = 12,
                  plotOutput("plot_lineal")
                )
              )
      ),
      # Panel: Gráfico de Barras
      tabItem(tabName = "barras",
              fluidRow(
                box(
                  title = "Promedio Anual del IPC",
                  status = "info", solidHeader = TRUE, width = 12,
                  plotOutput("plot_barras")
                )
              )
      ),
      # Panel: Gráfico de Torta
      tabItem(tabName = "torta",
              fluidRow(
                box(
                  title = "Distribución Ficticia por Rubro",
                  status = "warning", solidHeader = TRUE, width = 12,
                  plotOutput("plot_torta"),
                  helpText("Datos simulados para mostrar proporciones.")
                )
              )
      )
    )
  )
)

# LÓGICA DEL SERVIDOR
server <- function(input, output, session) {

  # Datos simulados para 6 años de IPC mensual (2017-2022)
  ipc_manual <- data.frame(
    fecha = seq(as.Date("2017-01-01"), as.Date("2022-12-01"), by = "month"),
    valor = c(
      1.6, 2.1, 2.3, 2.0, 1.9, 1.8, 2.2, 1.7, 1.9, 2.0, 2.1, 2.0, # 2017
      1.8, 2.0, 2.5, 2.3, 2.1, 2.4, 2.7, 2.5, 2.2, 2.3, 2.0, 1.9, # 2018
      2.5, 2.7, 2.9, 3.0, 3.2, 3.5, 3.3, 3.1, 3.0, 2.8, 2.6, 2.4, # 2019
      2.2, 2.0, 1.8, 1.6, 1.5, 1.3, 1.2, 1.0, 0.9, 1.2, 1.5, 1.8, # 2020 (año COVID)
      2.0, 2.3, 2.6, 2.9, 3.0, 3.2, 3.3, 3.5, 3.7, 3.9, 4.0, 4.2, # 2021
      4.5, 4.7, 4.9, 5.0, 5.1, 5.3, 5.5, 5.6, 5.8, 6.0, 6.2, 6.5  # 2022
    )
  )

  # Gráfico de Línea
  output$plot_lineal <- renderPlot({
    df <- ipc_manual

    ggplot(df, aes(x = fecha, y = valor)) +
      geom_line(color = "steelblue", size = 1.2) +
      geom_point(size = 1.5, color = "steelblue") +
      labs(title = "Variación Mensual del IPC (simulado)",
           x = "Fecha", y = "Porcentaje (%)") +
      scale_y_continuous(labels = function(x) paste0(x, "%")) +
      theme_minimal()
  })

  # Gráfico de Barras
  output$plot_barras <- renderPlot({
    df <- ipc_manual
    df$anio <- format(df$fecha, "%Y")

    df_anual <- df %>%
      group_by(anio) %>%
      summarise(promedio = mean(valor))

    ggplot(df_anual, aes(x = anio, y = promedio, fill = anio)) +
      geom_bar(stat = "identity", width = 0.6) +
      geom_text(aes(label = paste0(round(promedio, 1), "%")),
                vjust = -0.5, size = 4, color = "black") +
      labs(title = "Promedio Anual de la Variación del IPC (simulado)",
           x = "Año", y = "Promedio (%)") +
      scale_y_continuous(labels = function(x) paste0(x, "%"),
                         expand = expansion(mult = c(0, 0.1))) +
      theme_minimal() +
      theme(legend.position = "none")
  })

  # Gráfico de Torta
  output$plot_torta <- renderPlot({
    rubros <- data.frame(
      categoria = c("Alimentos", "Vivienda", "Salud", "Transporte", "Educación", "Entretenimiento"),
      porcentaje = c(20, 25, 15, 20, 10, 10)
    )

    rubros <- rubros %>%
      arrange(desc(categoria)) %>%
      mutate(
        fraccion = porcentaje / sum(porcentaje),
        ymax = cumsum(fraccion),
        ymin = c(0, head(ymax, n = -1)),
        label_pos = (ymax + ymin) / 2,
        label = paste0(round(fraccion * 100), "%")
      )

    ggplot(rubros, aes(ymax = ymax, ymin = ymin, xmax = 4, xmin = 3, fill = categoria)) +
      geom_rect() +
      coord_polar(theta = "y") +
      xlim(c(2, 4)) +
      theme_void() +
      labs(title = "Participación de Rubros en el IPC (ficticio)") +
      geom_text(aes(x = 3.5, y = label_pos, label = label), color = "white", size = 4)
  })
}

# EJECUCIÓN DE LA APLICACIÓN
shinyApp(ui, server)