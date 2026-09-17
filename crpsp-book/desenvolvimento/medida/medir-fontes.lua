-- medir-fontes.lua
-- Lado Lua da sonda de métricas. Carregado por medir-fontes.tex.
--
-- Em arquivo separado de propósito: dentro de \directlua o `%` é
-- comentário de TeX e decapitaria qualquer string.format("%.3f", ...).

crpsp = {}

local function mm(sp) return sp / 65536 * 25.4 / 72.27 end
local function pt(sp) return sp / 65536 end
local function f(x, n) return string.format("%." .. n .. "f", x) end

crpsp.metricas = io.open("medidas-fontes.tsv", "w")
crpsp.mancha   = io.open("medidas-mancha.tsv", "w")

crpsp.metricas:write(table.concat({
  "fonte", "corpo_pt", "altura_x_mm", "maiuscula_mm", "eme_pt",
  "x_eme", "maiusc_eme", "x_maiusc", "mm_por_car",
  "car80_mm", "car70_mm", "car60_mm", "car45_mm", "rnib", "face"
}, "\t") .. "\n")

crpsp.mancha:write(table.concat({
  "fonte", "corpo_pt", "mancha_mm", "caracteres"
}, "\t") .. "\n")

-- Manchas em disputa, em mm:
--    98,7  cartilha A5 hoje        105 / 110  cartilha A5 alargada
--   144    manual A4 (~70 car.)    164        relatorio A4 (80 car.)
crpsp.manchas = {98.7, 105, 110, 144, 164}

-- Limiares da RNIB para altura-x: 2,3 mm é a meta, 2,0 mm o mínimo.
local function rnib(xmm)
  if xmm >= 2.3 then return "meta" end
  if xmm >= 2.0 then return "minimo" end
  return "ABAIXO"
end

-- Uma medição: recebe sp inteiros do TeX e emite as duas linhas de saída.
function crpsp.row(rotulo, corpo, xsp, emsp, capsp, amsp, ncar, face)
  local xmm, capmm, empt = mm(xsp), mm(capsp), pt(emsp)
  local porcar = mm(amsp) / ncar
  crpsp.metricas:write(table.concat({
    rotulo, f(corpo, 2), f(xmm, 3), f(capmm, 3), f(empt, 2),
    f(xsp / emsp, 3), f(capsp / emsp, 3), f(xsp / capsp, 3), f(porcar, 4),
    f(porcar * 80, 1), f(porcar * 70, 1), f(porcar * 60, 1), f(porcar * 45, 1),
    rnib(xmm), face
  }, "\t") .. "\n")
  for _, largura in ipairs(crpsp.manchas) do
    crpsp.mancha:write(table.concat({
      rotulo, f(corpo, 2), f(largura, 1),
      tostring(math.floor(largura / porcar))
    }, "\t") .. "\n")
  end
end

function crpsp.fechar()
  crpsp.metricas:close()
  crpsp.mancha:close()
end
